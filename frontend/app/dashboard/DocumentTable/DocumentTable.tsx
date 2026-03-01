// SPDX-License-Identifier: Apache-2.0

"use client";

import { type JSX } from "react";
import { FaFileAlt, FaFilePowerpoint } from "react-icons/fa";
import { GrCode, GrDocumentOutlook, GrDocumentCsv, GrDocumentExcel, GrDocumentNotes, GrDocumentPdf, GrDocumentTxt, GrDocumentWord, GrImage } from "react-icons/gr";
import { LuCodeXml, LuFileJson } from "react-icons/lu";
import { RiFolderZipFill } from "react-icons/ri";

export default function DocumentTable({ results }: { results: Record<string, unknown>[] }) {
    if (results!= null && results.length == 0) return <p>No documents found</p>;

    const ICON_SIZE = 30;
    const iconos: Record<string, JSX.Element> = {
        // Office
        "docx":       <GrDocumentWord color="#2B579A" size={ICON_SIZE} />,
        "doc":        <GrDocumentWord color="#2B579A" size={ICON_SIZE} />,
        "xlsx":       <GrDocumentExcel color="#217346" size={ICON_SIZE} />,
        "xls":        <GrDocumentExcel color="#217346" size={ICON_SIZE} />,
        "pptx":       <FaFilePowerpoint color="#D24726" size={ICON_SIZE} />,
        "ppt":        <FaFilePowerpoint color="#D24726" size={ICON_SIZE} />,
        "one":        <GrDocumentNotes color="#7719AA" size={ICON_SIZE} />,
        "msg":        <GrDocumentOutlook color="#0072C6" size={ICON_SIZE} />,
        "eml":        <GrDocumentOutlook color="#0072C6" size={ICON_SIZE} />,
        // PDF
        "pdf":        <GrDocumentPdf color="#FF0000" size={ICON_SIZE} />,
        // Texto
        "txt":        <GrDocumentTxt color="#757575" size={ICON_SIZE} />,
        "csv":        <GrDocumentCsv color="#217346" size={ICON_SIZE} />,
        "xml":        <LuCodeXml color="#F16529" size={ICON_SIZE} />,
        "json":       <LuFileJson color="#F4A500" size={ICON_SIZE} />,
        // Imágenes
        "jpg":        <GrImage color="#F4A500" size={ICON_SIZE} />,
        "jpeg":       <GrImage color="#F4A500" size={ICON_SIZE} />,
        "png":        <GrImage color="#F4A500" size={ICON_SIZE} />,
        "gif":        <GrImage color="#F4A500" size={ICON_SIZE} />,
        "svg":        <GrImage color="#F4A500" size={ICON_SIZE} />,
        "webp":       <GrImage color="#F4A500" size={ICON_SIZE} />,
        "tiff":       <GrImage color="#F4A500" size={ICON_SIZE} />,
        // Comprimidos
        "zip":        <RiFolderZipFill color="#F4A500" size={ICON_SIZE} />,
        "rar":        <RiFolderZipFill color="#F4A500" size={ICON_SIZE} />,
        // Código
        "js":         <GrCode color="#F7DF1E" size={ICON_SIZE} />,
        "ts":         <GrCode color="#3178C6" size={ICON_SIZE} />,
        "py":         <GrCode color="#3776AB" size={ICON_SIZE} />,
        "html":       <GrCode color="#F16529" size={ICON_SIZE} />,
        "css":        <GrCode color="#264DE4" size={ICON_SIZE} />,
    };
    //Recibe los datos y muestra la tabla
    return (
        <div className="documents-css">
            {results.map((row, i) => {
                const values = Object.values(row)
                const firstValue = String(values[0])
                const rest = values.slice(1).map((v) => String(v)).join(" - ")
                return (
                    <div key={i} className="documents-row-css">
                        <div>
                            <h4 className="font-bold">{firstValue}</h4>
                            <div className="flex flex-wrap">
                                {rest.split(" - ").map((item, index) => {
                                    const isLink = item.startsWith("http://") || item.startsWith("https://");
                                    return (
                                        <span key={index} className="mini-tag border rounded px-4 py-0.5 m-1">
                                            {isLink ? (
                                                <a href={item} target="_blank" rel="noopener noreferrer">Link al documento</a>
                                            ) : (
                                                item
                                            )}
                                        </span>
                                    );
                                })}
                            </div>
                        </div>
                        <div>
                            {iconos[String(row["extension"])] || <FaFileAlt size={ICON_SIZE} />}
                        </div>
                    </div>
                );
            })}
        </div>
    );
}