// SPDX-License-Identifier: Apache-2.0

"use client";

import { type JSX } from "react";
import { FaFileAlt, FaFilePowerpoint } from "react-icons/fa";
import { GrCode, GrDocumentOutlook, GrDocumentCsv, GrDocumentExcel, GrDocumentNotes, GrDocumentPdf, GrDocumentTxt, GrDocumentWord, GrImage } from "react-icons/gr";
import { LuCodeXml, LuFileJson } from "react-icons/lu";
import { RiFolderZipFill } from "react-icons/ri";
import { SiGoogledocs, SiGoogleforms, SiGooglesheets, SiGoogleslides } from "react-icons/si";

export default function DocumentTable({ results }: { results: Record<string, unknown>[] }) {
    //Si la tabla es vacia no se genera nada
    if (results.length === 0) return <p>No documents found</p>; //TODO: Revisar CSS

    const ICON_SIZE = 30;
    const iconos: Record<string, JSX.Element> = {
        // Office
        "Word":       <GrDocumentWord color="#2B579A" size={ICON_SIZE} />,
        "Excel":      <GrDocumentExcel color="#217346" size={ICON_SIZE} />,
        "PowerPoint": <FaFilePowerpoint color="#D24726" size={ICON_SIZE} />,
        "OneNote":    <GrDocumentNotes color="#7719AA" size={ICON_SIZE} />,
        "Outlook":    <GrDocumentOutlook color="#0072C6" size={ICON_SIZE} />,
        // Google
        "Docs":       <SiGoogledocs color="#4285F4" size={ICON_SIZE} />,
        "Sheets":     <SiGooglesheets color="#0F9D58" size={ICON_SIZE} />,
        "Slides":     <SiGoogleslides color="#F4B400" size={ICON_SIZE} />,
        "Forms":      <SiGoogleforms color="#7B4EA6" size={ICON_SIZE} />,
        // PDF
        "PDF":        <GrDocumentPdf color="#FF0000" size={ICON_SIZE} />,
        // Texto
        "TXT":        <GrDocumentTxt color="#757575" size={ICON_SIZE} />,
        "CSV":        <GrDocumentCsv color="#217346" size={ICON_SIZE} />,
        "XML":        <LuCodeXml color="#F16529" size={ICON_SIZE} />,
        "JSON":       <LuFileJson color="#F4A500" size={ICON_SIZE} />,
        // Imágenes
        "JPG":        <GrImage color="#F4A500" size={ICON_SIZE} />,
        "JPEG":       <GrImage color="#F4A500" size={ICON_SIZE} />,
        "PNG":        <GrImage color="#F4A500" size={ICON_SIZE} />,
        "GIF":        <GrImage color="#F4A500" size={ICON_SIZE} />,
        "SVG":        <GrImage color="#F4A500" size={ICON_SIZE} />,
        "WEBP":       <GrImage color="#F4A500" size={ICON_SIZE} />,
        "TIFF":       <GrImage color="#F4A500" size={ICON_SIZE} />,
        // Comprimidos
        "ZIP":        <RiFolderZipFill color="#F4A500" size={ICON_SIZE} />,
        "RAR":        <RiFolderZipFill color="#F4A500" size={ICON_SIZE} />,
        // Código
        "JS":         <GrCode color="#F7DF1E" size={ICON_SIZE} />,
        "TS":         <GrCode color="#3178C6" size={ICON_SIZE} />,
        "PY":         <GrCode color="#3776AB" size={ICON_SIZE} />,
        "HTML":       <GrCode color="#F16529" size={ICON_SIZE} />,
        "CSS":        <GrCode color="#264DE4" size={ICON_SIZE} />,
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
                            <p>{rest}</p>
                        </div>
                        <div>
                            {iconos[String(row["type"])] || <FaFileAlt size={ICON_SIZE} />}
                        </div>
                    </div>
                );
            })}
        </div>
    );
}