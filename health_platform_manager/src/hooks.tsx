import * as AWS from "aws-sdk";
import {
    createContext,
    useCallback,
    useContext,
    useEffect,
    useState,
} from "react";

import { ListDigitalTwin, DigitalTwin } from "./types/DigitalTwin";
import { docClient } from "./services/aws";

AWS.config.update({
    region: "eu-west-2",
    accessKeyId: process.env.REACT_APP_AWS_PUBLIC_KEY,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_KEY,
});

interface DigitalTwinSetter {
    setFullDigitalTwin: (digitalTwin: DigitalTwin | null) => void;
}

interface Parameters {
    TableName: string;
    ProjectionExpression: string;
    ExpressionAttributeNames: {
        "#i": string;
    };
    Limit: number;
    ExclusiveStartKey?: { [key: string]: string };
}

export function useDigitalTwins(
    maxDigitalTwins: number = 10,
    page: number = 1
): [ListDigitalTwin[] | undefined, boolean] {
    const [digitalTwins, setDigitalTwins] = useState<ListDigitalTwin[]>([]);
    const [digitalTwinPageKeys, setDigitalTwinPageKeys] = useState<string[]>(
        []
    );
    const [digitalTwinPageSet, setDigitalTwinPageSet] = useState<
        ListDigitalTwin[]
    >([]);
    const [lastPage, setLastPage] = useState<boolean>(false);

    useEffect((): void => {
        if (page > digitalTwinPageKeys.length) {
            let params: Parameters = {
                TableName: "DigitalTwins",
                ProjectionExpression: "#i, firstname, lastname",
                ExpressionAttributeNames: { "#i": "uuid" },
                Limit: maxDigitalTwins,
            };

            if (page > 1)
                params["ExclusiveStartKey"] = {
                    uuid: digitalTwinPageKeys[page - 2],
                };

            docClient.scan(params, function (err, data) {
                if (err) {
                    console.error(err);
                } else {
                    if (data.Items?.length) {
                        setDigitalTwins((digitalTwins) => [
                            ...digitalTwins,
                            ...(data.Items as ListDigitalTwin[]),
                        ]);
                        setDigitalTwinPageSet(data.Items as ListDigitalTwin[]);
                    } else {
                        setLastPage(
                            digitalTwinPageKeys[page - 1] === null ||
                                page > digitalTwinPageKeys.length
                        );
                        setDigitalTwinPageSet([]);
                        return;
                    }

                    const newKey = data.LastEvaluatedKey
                        ? data.LastEvaluatedKey["uuid"]
                        : null;

                    if (
                        (newKey && !digitalTwinPageKeys.includes(newKey)) ||
                        (newKey === null &&
                            !digitalTwinPageKeys[
                                digitalTwinPageKeys.length - 1
                            ] !== null)
                    )
                        setDigitalTwinPageKeys((digitalTwinPageKeys) => [
                            ...digitalTwinPageKeys,
                            newKey,
                        ]);
                }
            });
        } else {
            setLastPage(
                digitalTwinPageKeys[page - 1] === null ||
                    page > digitalTwinPageKeys.length
            );
            setDigitalTwinPageSet(
                digitalTwins.slice(
                    (page - 1) * maxDigitalTwins,
                    page * maxDigitalTwins
                )
            );
        }
    }, [maxDigitalTwins, page]);

    return [digitalTwinPageSet, lastPage];
}

export function useDigitalTwin(
    uuid: string
): [DigitalTwin | null | undefined, DigitalTwinSetter] {
    const [digitalTwin, setDigitalTwin] = useState<DigitalTwin | null>();

    useEffect((): void => {
        let params = {
            TableName: "DigitalTwins",
            Key: { uuid: uuid },
        };

        docClient.get(params, function (err, data) {
            if (err) {
                console.error(err);
            } else {
                data.Item
                    ? setDigitalTwin(data.Item as DigitalTwin)
                    : setDigitalTwin(null);
            }
        });
    }, [uuid]);

    const setFullDigitalTwin = useCallback(
        (digitalTwin: DigitalTwin | null): void => {
            setDigitalTwin(digitalTwin);
        },
        []
    );

    return [digitalTwin, { setFullDigitalTwin }];
}

export const DigitalTwinContext = createContext<
    [DigitalTwin | null, DigitalTwinSetter]
>([null, { setFullDigitalTwin: (): void => undefined }]);

export function useDigitalTwinContext(): [
    DigitalTwin | null,
    DigitalTwinSetter
] {
    return useContext(DigitalTwinContext);
}
