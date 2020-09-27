import { Appendices } from "./Appendices";

export interface User {
    uuid: string;
    age: number;
    sex: string;
    firstname: string;
    lastname: string;
    conditions: string[];
    appendices: Appendices;
}

export interface ListUser {
    uuid: string;
    firstname: string;
    lastname: string;
}
