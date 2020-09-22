export interface User {
    uuid: string;
    age: number;
    firstname: string;
    lastname: string;
    conditions: string[];
    appendices: Appendices;
}

interface Appendices {
    lastchanged: Date;
    appendices: { [uuid: string]: Appendix };
}

interface Appendix {
    uuid: string;
    created: Date;
    lastchanged: Date;
    value: any;
}
