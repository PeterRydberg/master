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
        [key: string]: {
            [maptype: string]:
                | { [type: string]: number | string }
                | number
                | string;
        };
    };
}

function updateAWSUser(params: Parameters): User | void {
    docClient.update(params, function (err, data) {
        if (err) {
            throw err;
        } else {
            return data;
        }
    });
}

export function updateUserAttribute(
    uuid: string,
    attribute: string,
    value: string
): User | void {
    let params: Parameters = {
        TableName: "Users",
        Key: { uuid: uuid },
        ReturnValues: "ALL_NEW",
        UpdateExpression: `set ${attribute} = ${value}`,
    };

    return updateAWSUser(params);
}

export function addAWSAppendix(
    uuid: string,
    attribute: string,
    value: Appendix
): User | void {
    makeAppendices(uuid);
    makeAttribute(uuid, attribute);
    return makeUuid(uuid, attribute, value);
}

export function makeUuid(
    uuid: string,
    attribute: string,
    value: Appendix
): User | void {
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
            ":date": { N: Date.now() },
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
            ":date": { N: Date.now() },
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
            ":date": { N: Date.now() },
        },
    };

    updateAWSUser(params);
}
