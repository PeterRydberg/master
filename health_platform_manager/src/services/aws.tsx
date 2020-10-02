import * as AWS from "aws-sdk";

import { v4 as uuidv4 } from "uuid";
import { Appendix } from "../types/Appendices";

import { User } from "./../types/User";

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

async function updateAWSUser(params: Parameters): Promise<User | void> {
    return docClient
        .update(params)
        .promise()
        .then((data) => {
            return data.Attributes as User;
        })
        .catch((error) => {
            console.error(error);
        });
}

export async function updateUserAttribute(
    uuid: string,
    attributes: string[],
    value: string | boolean | number
): Promise<User | void> {
    const [attributeDict, attributeString] = spreadAttributes(attributes);

    let params: Parameters = {
        TableName: "Users",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `set ${attributeString} = :val`,
        ExpressionAttributeNames: attributeDict,
        ExpressionAttributeValues: {
            ":val": value,
        },
    };

    return updateAWSUser(params);
}

export async function addAWSAppendix(
    uuid: string,
    attribute: string,
    value: Appendix
): Promise<User | void> {
    makeAppendices(uuid);
    makeAttribute(uuid, attribute);
    return makeUuid(uuid, attribute, value);
}

export async function makeUuid(
    uuid: string,
    attribute: string,
    value: Appendix
): Promise<User | void> {
    let params: Parameters = {
        TableName: "Users",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `
            SET appendices.lastchanged = :date,
            appendices.appendices.#attribute.#uuid = if_not_exists(appendices.appendices.#attribute.#uuid, :appendix)
            `,
        ExpressionAttributeNames: {
            "#uuid": uuidv4(),
            "#attribute": attribute,
        },
        ExpressionAttributeValues: {
            ":date": Date.now(),
            ":appendix": {
                created: value.created,
                lastchanged: value.lastchanged,
                value: value.value,
            },
        },
    };

    return updateAWSUser(params);
}

export function makeAttribute(uuid: string, attribute: string): void {
    let params: Parameters = {
        TableName: "Users",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `
            SET appendices.lastchanged = :date,
            appendices.appendices.#attribute = if_not_exists(appendices.appendices.#attribute, :emptymap)
            `,
        ExpressionAttributeNames: {
            "#attribute": attribute,
        },
        ExpressionAttributeValues: {
            ":emptymap": {},
            ":date": Date.now(),
        },
    };

    updateAWSUser(params);
}

export function makeAppendices(uuid: string): void {
    let params: Parameters = {
        TableName: "Users",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `
            SET appendices.lastchanged = :date,
            appendices.appendices = if_not_exists(appendices.appendices, :emptymap)
            `,
        ExpressionAttributeValues: {
            ":emptymap": {},
            ":date": Date.now(),
        },
    };

    updateAWSUser(params);
}
