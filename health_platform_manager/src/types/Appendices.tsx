export interface Appendices {
    lastchanged: Date;
    appendices: {
        [appendixType: string]: {
            [uuid: string]: Appendix;
        };
    };
}

export interface Appendix {
    uuid: string;
    created: Date;
    lastchanged: Date;
    value: any;
}
