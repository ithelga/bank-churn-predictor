import { useState, useRef } from "react";
import { useRouter } from "next/router";
import Header from "@/components/header";
import styles from "@/styles/Home.module.css";
import request from "@/pages/api/request";

export default function Home() {
    const [status, setStatus] = useState("idle");
    const [processedCount, setProcessedCount] = useState(0);
    const fileInputRef = useRef(null);
    const router = useRouter();
    const [fileUid, setFileUid] = useState(null);
    const [errorMsg, setErrorMsg] = useState("");

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setStatus("processing");
        setErrorMsg("");

        const formData = new FormData();
        formData.append("file", file);

        try {
            const jsonData = await request.post("/fine-tune/", formData);
            setProcessedCount(jsonData.count);
            setFileUid(jsonData.file_uid);
            setStatus("done");
        } catch (error) {
            console.error("Error uploading file:", error);
            setStatus("idle");

            if (error.message.includes("Only CSV files are supported")) {
                setErrorMsg("❌ Пожалуйста, загрузите файл в формате CSV");
            } else if (error.message.includes("Missing required columns")) {
                const detailStart = error.message.indexOf("Missing required columns:");
                if (detailStart !== -1) {
                    const rawDetail = error.message.slice(detailStart);
                    const columnList = rawDetail
                        .replace("Missing required columns:", "")
                        .trim()
                        .slice(0, -4);  // убираем последние 4 символа
                    setErrorMsg(`❌ Пропущены обязательные колонки: ${columnList}`);
                }
            } else {
                setErrorMsg("❌ Не удалось обработать файл. Попробуйте позже.");
            }
        }

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };


    const handleNavigateToAnalytics = () => {
        if (fileUid) {
            router.push({
                pathname: "/analytics",
                query: { file_uid: fileUid },
            });
        }
    };


    return (
        <>
            <Header />
            <div className={styles.wrapper}>
                <div className={styles.formContainer}>
                    <img src="/logo.png" alt="Логотип" className={styles.logo} />



                    {status === "idle" && (
                        <div className={styles.contentBottom}>
                            <h2 className={styles.title}>Загрузите информацию по вашим клиентам</h2>
                            <p className={styles.subtitle}>Формат: CSV</p>
                            <label className={styles.uploadButton}>
                                Загрузить файл
                                <input
                                    type="file"
                                    accept=".csv"
                                    onChange={handleFileUpload}
                                    className={styles.hiddenInput}
                                    ref={fileInputRef}
                                />
                            </label>
                        </div>
                    )}



                    {status === "processing" && (
                        <div className={styles.processingContainer}>
                            <div className={styles.spinner}></div>
                            <p className={styles.processingText}>Обработка файла...</p>
                        </div>
                    )}

                    {errorMsg && <p className={styles.errorText}>{errorMsg}</p>}

                    {status === "done" && (
                        <div className={styles.contentBottom}>
                            <h2 className={styles.resultTitle}>Обработано {processedCount} клиентов</h2>
                            <button className={styles.detailButton} onClick={handleNavigateToAnalytics}>
                                Изучить подробнее
                            </button>
                        </div>
                    )}


                </div>

            </div>
        </>
    );
}
