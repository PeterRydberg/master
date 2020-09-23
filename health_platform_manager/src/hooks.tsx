import * as AWS from "aws-sdk";
import { useEffect, useState } from "react";

import { User } from "./types/User";

AWS.config.update({
    region: "eu-west-2",
    accessKeyId: process.env.REACT_APP_AWS_PUBLIC_KEY,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_KEY,
});

const docClient = new AWS.DynamoDB.DocumentClient();

export function useUsers(): User[] | undefined | null {
    const [users, setUsers] = useState<User[] | null>();
    useEffect((): void => {
        let params = {
            TableName: "Users",
        };

        docClient.scan(params, function (err, data) {
            if (err) {
                console.log(err);
            } else {
                data.Items ? setUsers(data.Items as User[]) : setUsers(null);
            }
        });
    }, []);
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
