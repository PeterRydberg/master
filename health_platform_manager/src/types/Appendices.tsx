export interface Appendices {
    lastchanged: number;
    appendices: {
        [appendixType: string]: {
            [uuid: string]: Appendix;
        };
    };
}

export interface Appendix {
    created: number;
    lastchanged: number;
    value: any;
}
