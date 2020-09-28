import React, { useState } from "react";
import { Appendices } from "../../../types/Appendices";

import "./styles.css";

function useInput(
    inputProps: FileProps,
    inputType?: string
): { inputValue: string; inputElement: JSX.Element } {
    const [inputValue, setInputValue] = useState<string>("");

    /*if (inputType)
        inputProps["accept"] = `${inputType}\\${inputProps["accept"]
            .split("\\")
            .pop()}`;*/

    const inputElement = (
        <input
            {...inputProps}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
        />
    );
    return { inputValue, inputElement };
}

function useSelect(
    selectProps: DropdownProps,
    options: string[]
): { selectValue: string; selectElement: JSX.Element } {
    const [selectValue, setSelectValue] = useState(options[0]);
    const selectElement = (
        <select
            {...selectProps}
            value={selectValue}
            onChange={(e) => setSelectValue(e.target.value)}
        >
            {options.map((element) => (
                <option key={element} value={element}>
                    {element}
                </option>
            ))}
        </select>
    );
    return { selectValue, selectElement };
}

function createFilePath(
    filename: string,
    filetype: string,
    full?: boolean
): string {
    const paths = filename.split("\\");
    const file = paths ? paths[paths.length - 1] : "";

    const ending = `${process.env.REACT_APP_DATA_SOURCE_PATH}${filetype}\\${file}`;
    if (full) return `${process.env.REACT_APP_FULL_DIRECTORY_PATH}${ending}`;
    return `${ending}`;
}

const fileProps: FileProps = {
    type: "file",
    id: "appendix_paths",
    accept: ".nii.gz",
    multiple: false,
};

const dropdownProps: DropdownProps = {
    autoFocus: false,
    disabled: false,
    multiple: false,
    required: true,
};

const dropdownOptions: string[] = [
    "heart",
    "braintumour",
    "hippocampus",
    "prostate",
];

function AppendicesList({ appendices, className }: Props): JSX.Element {
    const { selectValue, selectElement } = useSelect(
        dropdownProps,
        dropdownOptions
    );
    const { inputValue, inputElement } = useInput(fileProps, selectValue);

    const content = !Object.keys(appendices).length ? (
        <span>No appendices to show.</span>
    ) : (
        Object.entries(appendices.appendices).map(([key, appendixList]) => (
            <div>
                <h3>Type {key}:</h3>
                <div key={key}>
                    {Object.entries(appendixList).map(([name, appendix]) => (
                        <div key={name}>
                            <h4>Appendix name {name}:</h4>
                            <p>Created: {appendix.created}</p>
                            <p>Last changed: {appendix.lastchanged}</p>
                            <p>Contents: {appendix.value}</p>
                        </div>
                    ))}
                </div>
            </div>
        ))
    );

    return (
        <div className={`appendices-list ${className || ""}`}>
            {content}
            <div className="appendix-adder">
                <label>Add appendix: </label>
                {selectElement}
                {inputElement}
                <button disabled={!inputValue || !selectValue}>Submit</button>
            </div>
        </div>
    );
}

interface Props {
    appendices: Appendices;
    className?: string;
}

interface FileProps {
    type: string;
    id: string;
    accept: string;
    multiple: boolean;
}

interface DropdownProps {
    autoFocus: boolean;
    disabled: boolean;
    multiple: boolean;
    required: boolean;
}

export default AppendicesList;
