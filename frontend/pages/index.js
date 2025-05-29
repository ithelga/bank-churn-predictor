import { useState, useRef } from "react";
import { useRouter } from "next/router";
import Header from "@/components/header";
import styles from "@/styles/Home.module.css";
import request from "@/pages/api/request";

export default function Home() {
    const [status, setStatus] = useState("idle");
    const [processedCount, setProcessedCount] = useState(0);
    const [resultData, setResultData] = useState(null);
    const fileInputRef = useRef(null);
    const router = useRouter();

    async function loadData() {
        try {
            const jsonData = await request.get('/test-evaluate/');
            const count = jsonData.count;
            setProcessedCount(count);
            setResultData(jsonData); // сохраняем весь объект
            setStatus("done");
        } catch (error) {
            console.error("Error fetching data:", error);
            setStatus("idle");
        }
    }

    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setStatus("processing");
            loadData();
        }

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    const handleNavigateToAnalytics = () => {
        if (resultData) {
            router.push({
                pathname: "/analytics",
                query: { data: JSON.stringify(resultData) },
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
