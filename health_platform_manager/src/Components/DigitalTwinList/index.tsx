import React from "react";

import * as AWS from "aws-sdk";

import "./styles.css";

AWS.config.update({
  region: "eu-west-2",
  //endpoint: "dynamodb.eu-west-2.amazonaws.com",
  accessKeyId: process.env.REACT_APP_AWS_PUBLIC_KEY,
  secretAccessKey: process.env.REACT_APP_AWS_SECRET_KEY,
});

const dynamodb = new AWS.DynamoDB();
const docClient = new AWS.DynamoDB.DocumentClient();

function DigitalTwinList({ className }: Props): JSX.Element {
  const read = (): string[] => {
    let params = {
      TableName: "User",
    };

    docClient.scan(params, function (err, data) {
      if (err) {
        console.log(err);
      } else {
        return data;
      }
    });
    return [];
  };

  return (
    <div className={`digital-twin-list ${className || ""}`}>
      <ul>
        <li>{process.env.REACT_APP_AWS_PUBLIC_KEY}</li>
      </ul>
    </div>
  );
}

interface Props {
  className?: string;
}

export default DigitalTwinList;
