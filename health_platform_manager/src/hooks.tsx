import * as AWS from "aws-sdk";
import { useEffect, useState } from "react";

import { ListUser, User } from "./types/User";

AWS.config.update({
    region: "eu-west-2",
    accessKeyId: process.env.REACT_APP_AWS_PUBLIC_KEY,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_KEY,
});

const docClient = new AWS.DynamoDB.DocumentClient();

interface Parameters {
    TableName: string;
    ProjectionExpression: string;
    ExpressionAttributeNames: {
        "#i": string;
    };
    Limit: number;
    ExclusiveStartKey?: { [key: string]: string };
}

export function useUsers(
    maxUsers: number = 10,
    page: number = 1
): ListUser[] | undefined | null {
    const [users, setUsers] = useState<ListUser[] | null>();
    const [userPageKeys, setUserPageKeys] = useState<string[]>([]);
    useEffect((): void => {
        let params: Parameters = {
            TableName: "Users",
            ProjectionExpression: "#i, firstname, lastname",
            ExpressionAttributeNames: { "#i": "uuid" },
            Limit: maxUsers,
        };

        if (page > 1)
            params["ExclusiveStartKey"] = { uuid: userPageKeys[page - 2] };

        docClient.scan(params, function (err, data) {
            if (err) {
                console.log(err);
            } else {
                data.Items
                    ? setUsers(data.Items as ListUser[])
                    : setUsers(null);

                const newKey = data.LastEvaluatedKey
                    ? data.LastEvaluatedKey["uuid"]
                    : null;
                if (newKey && !userPageKeys.includes(newKey))
                    setUserPageKeys([...userPageKeys, newKey]);
            }
        });
    }, [maxUsers, userPageKeys, page]);
    return users;
}

export function useUser(uuid: string): User | undefined | null {
    const [user, setUser] = useState<User | null>();
    useEffect((): void => {
        let params = {
            TableName: "Users",
            Key: { uuid: uuid },
        };

        docClient.get(params, function (err, data) {
            if (err) {
                console.log(err);
            } else {
                data.Item ? setUser(data.Item as User) : setUser(null);
            }
        });
    }, [uuid]);
    return user;
}
