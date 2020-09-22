import React, { useEffect, useState } from "react";

import * as AWS from "aws-sdk";

import { User } from "../../types/User";
import DigitalTwinListElement from "./DigitalTwinListElement";

import "./styles.css";

AWS.config.update({
    region: "eu-west-2",
    accessKeyId: process.env.REACT_APP_AWS_PUBLIC_KEY,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_KEY,
});

//const dynamodb = new AWS.DynamoDB();
const docClient = new AWS.DynamoDB.DocumentClient();

function DigitalTwinList({ className }: Props): JSX.Element {
    const [users, setUsers] = useState<User[]>([]);

    useEffect(() => {
        let params = {
            TableName: "Users",
        };

        docClient.scan(params, function (err, data) {
            if (err) {
                console.log(err);
            } else {
                setUsers(data.Items as User[]);
            }
        });
    }, []);

    const userList = users.map((user) => (
        <DigitalTwinListElement user={user} />
    ));

    return (
        <div className={`digital-twin-list ${className || ""}`}>
            <ul>{userList}</ul>
        </div>
    );
}

interface Props {
    className?: string;
}

export default DigitalTwinList;
