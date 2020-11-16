import * as AWS from "aws-sdk";

import { v4 as uuidv4 } from "uuid";
import { Image } from "../types/DicomScans";

import { DigitalTwin } from "../types/DigitalTwin";

AWS.config.update({
    region: "eu-west-2",
    accessKeyId: process.env.REACT_APP_AWS_PUBLIC_KEY,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_KEY,
});

export const docClient = new AWS.DynamoDB.DocumentClient();

interface Parameters {
    TableName: string;
    Key: { [key: string]: string };
    ReturnValues: string;
    UpdateExpression: string;
    ExpressionAttributeNames?: {
        [key: string]: string;
    };
    ExpressionAttributeValues?: {
        [key: string]:
            | {
                  [maptype: string]:
                      | { [type: string]: number | string }
                      | number
                      | string;
              }
            | any;
    };
}

function spreadAttributes(
    attributes: string[]
): [{ [key: string]: string }, string] {
    const attributeDict: { [key: string]: string } = {};
    let attributeString: string = "";

    attributes.forEach((element, index) => {
        const attrLetter = String.fromCharCode(97 + index);
        attributeDict[`#${attrLetter}`] = element;
        attributeString += `#${attrLetter}.`;
    });

    return [attributeDict, attributeString.slice(0, -1)];
}

async function updateAWSDigitalTwin(
    params: Parameters
): Promise<DigitalTwin | void> {
    return docClient
        .update(params)
        .promise()
        .then((data) => {
            return data.Attributes as DigitalTwin;
        })
        .catch((error) => {
            console.error(error);
        });
}

export async function updateDigitalTwinAttribute(
    uuid: string,
    attributes: string[],
    value: string | boolean | number,
    updateLastChanged?: boolean
    ): Promise<DigitalTwin | void> {
    const [attributeDict, attributeString] = spreadAttributes(attributes);
    
    let lastChangedString = ""
    if (updateLastChanged){
        attributeDict['#lastchanged'] = 'lastchanged';
        let lastChangedArray = attributeString.split('#')
        lastChangedArray.pop()
        lastChangedString = `, ${lastChangedArray.join("#")}#lastchanged = :date`
    }

    let params: Parameters = {
        TableName: "DigitalTwins",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `SET ${attributeString} = :val, dicom_scans.lastchanged = :date${lastChangedString}`,
        ExpressionAttributeNames: attributeDict,
        ExpressionAttributeValues: {
            ":val": value,
            ":date": Date.now()
        },
    };
    

    return updateAWSDigitalTwin(params);
}

export async function addAWSImage(
    uuid: string,
    attribute: string,
    image: Image
): Promise<DigitalTwin | void> {
    makeDicomScans(uuid);
    makeAttribute(uuid, attribute);
    return makeUuid(uuid, attribute, image);
}

export async function deleteAWSImage(
    uuid: string,
    attributes: string[]
):Promise<DigitalTwin | void> {
    const [attributeDict, attributeString] = spreadAttributes(attributes);

    let params: Parameters = {
        TableName: "DigitalTwins",
        Key: {
            uuid: uuid            
        },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `REMOVE ${attributeString}`,
        ExpressionAttributeNames: attributeDict,
    }

    return updateAWSDigitalTwin(params);
}

export async function makeUuid(
    uuid: string,
    attribute: string,
    image: Image
): Promise<DigitalTwin | void> {
    let params: Parameters = {
        TableName: "DigitalTwins",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `
            SET dicom_scans.lastchanged = :date,
            dicom_scans.dicom_categories.#attribute.#uuid = if_not_exists(dicom_scans.dicom_categories.#attribute.#uuid, :image)
            `,
        ExpressionAttributeNames: {
            "#uuid": uuidv4(),
            "#attribute": attribute,
        },
        ExpressionAttributeValues: {
            ":date": Date.now(),
            ":image": {
                created: image.created,
                lastchanged: image.lastchanged,
                image_path: image.image_path,
                segmentation_path: image.segmentation_path,
                inference_path: image.inference_path,
                aiaa_consented: image.aiaa_consented,
                aiaa_approved: image.aiaa_approved
            },
        },
    };

    return updateAWSDigitalTwin(params);
}

export function makeAttribute(uuid: string, attribute: string): void {
    let params: Parameters = {
        TableName: "DigitalTwins",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `
            SET dicom_scans.lastchanged = :date,
            dicom_scans.dicom_categories.#attribute = if_not_exists(dicom_scans.dicom_categories.#attribute, :emptymap)
            `,
        ExpressionAttributeNames: {
            "#attribute": attribute,
        },
        ExpressionAttributeValues: {
            ":emptymap": {},
            ":date": Date.now(),
        },
    };

    updateAWSDigitalTwin(params);
}

export function makeDicomScans(uuid: string): void {
    let params: Parameters = {
        TableName: "DigitalTwins",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `
            SET dicom_scans.lastchanged = :date,
            dicom_scans.dicom_categories = if_not_exists(dicom_scans.dicom_categories, :emptymap)
            `,
        ExpressionAttributeValues: {
            ":emptymap": {},
            ":date": Date.now(),
        },
    };

    updateAWSDigitalTwin(params);
}
