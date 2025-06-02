import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Header from "@/components/header";
import styles from "@/styles/Analytics.module.css";
import AnalyticsCharts from "@/components/AnalyticsCharts";
import request from "@/pages/api/request";

export default function Analytics() {
    const router = useRouter();
    const { file_uid } = router.query;
    const [view, setView] = useState("analytics");
    const [clientsInfo, setClientsInfo] = useState([]);
    const [analyticsData, setAnalyticsData] = useState(null);
    const [group, setGroup] = useState(0);

    const [loadingAnalytics, setLoadingAnalytics] = useState(false);
    const [loadingClients, setLoadingClients] = useState(false);

    const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

    const sortedClients = [...clientsInfo].sort((a, b) => {
        if (!sortConfig.key) return 0;

        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];

        if (typeof aValue === "string") {
            return sortConfig.direction === "asc"
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        }

        return sortConfig.direction === "asc" ? aValue - bValue : bValue - aValue;
    });

    const handleSort = (key) => {
        setSortConfig((prev) => {
            if (prev.key === key) {
                return { key, direction: prev.direction === "asc" ? "desc" : "asc" };
            }
            return { key, direction: "asc" };
        });
    };



    useEffect(() => {
        if (view === "analytics" && file_uid) {
            setLoadingAnalytics(true);
            request.get(`/analytics/${file_uid}`)
                .then(data => setAnalyticsData(data.analytics))
                .catch(err => console.error("Ошибка загрузки аналитики:", err))
                .finally(() => setLoadingAnalytics(false));
        }
    }, [view, file_uid]);

    useEffect(() => {
        if (view === "top" && file_uid) {
            setLoadingClients(true);
            request.get(`/clients-group/${file_uid}?group=${group}`)
                .then(data => setClientsInfo(data.clients_info))
                .catch(err => console.error("Ошибка загрузки клиентов:", err))
                .finally(() => setLoadingClients(false));
        }
    }, [view, file_uid, group]);

    const handleGroupClick = (g) => {
        setGroup(g);
    };

    const tableHeaders = [
        { label: "Фамилия", key: "Surname" },
        { label: "Кредитный рейтинг", key: "CreditScore" },
        { label: "Страна", key: "Geography" },
        { label: "Пол", key: "Gender" },
        { label: "Возраст", key: "Age" },
        { label: "Стаж", key: "Tenure" },
        { label: "Баланс", key: "Balance" },
        { label: "Кол-во продуктов", key: "NumOfProducts" },
        { label: "Кредитная карта", key: "HasCrCard" },
        { label: "Активный клиент", key: "IsActiveMember" },
        { label: "Оценочная зарплата", key: "EstimatedSalary" },
        { label: "Вероятность оттока", key: "ChurnProbability" },
    ];


    const translateCountry = (country) => {
        switch (country) {
            case "Germany": return "Германия";
            case "France": return "Франция";
            case "Spain": return "Испания";
            default: return country;
        }
    };

    const translateGender = (gender) =>
        gender === "Male" ? "Мужской" : "Женский";

    return (
        <>
            <Header />
            <div className={styles.container}>
                <div className={styles.navButtons}>
                    <a
                        href="#"
                        className={`${styles.link} ${view === "analytics" ? styles.active : ""}`}
                        onClick={(e) => {
                            e.preventDefault();
                            setView("analytics");
                        }}
                    >
                        АНАЛИТИКА
                    </a>
                    <a
                        href="#"
                        className={`${styles.link} ${view === "top" ? styles.active : ""}`}
                        onClick={(e) => {
                            e.preventDefault();
                            setView("top");
                        }}
                    >
                        ТОП КЛИЕНТОВ
                    </a>
                </div>

                {view === "analytics" && (
                    loadingAnalytics ? (
                        <div className={styles.processingContainer}>
                            <div className={styles.spinner}></div>
                            <p className={styles.processingText}>Загрузка аналитики...</p>
                        </div>
                    ) : (
                        analyticsData && <AnalyticsCharts data={analyticsData} />
                    )
                )}


                {view === "top" && (
                    loadingClients ? (
                        <div className={styles.processingContainer}>
                            <div className={styles.spinner}></div>
                            <p className={styles.processingText}>Загрузка клиентов...</p>
                        </div>
                    ) : (
                        <>
                            <div className={styles.topHeader}>
                                <div className={styles.clientCount}>
                                    Клиентов: {clientsInfo.length}
                                </div>
                                <div className={styles.groupButtons}>
                                    {[0, 1, 2, 3, 4].map(g => (
                                        <button
                                            key={g}
                                            className={`${styles.groupButton} ${group === g ? styles.activeGroup : ""}`}
                                            onClick={() => setGroup(g)}
                                        >
                                            {{
                                                0: "Все",
                                                1: "0–25%",
                                                2: "25–50%",
                                                3: "50–75%",
                                                4: "75–100%"
                                            }[g]}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div style={{ overflowX: "auto" }}>
                                <table className={styles.table}>
                                    <thead>
                                    <tr>
                                        {tableHeaders.map(({ label, key }) => (
                                            <th
                                                key={key}
                                                onClick={() => handleSort(key)}
                                                style={{ cursor: "pointer" }}
                                            >
                                                {label}
                                                {sortConfig.key === key && (
                                                    <span>{sortConfig.direction === "asc" ? " ▲" : " ▼"}</span>
                                                )}
                                            </th>
                                        ))}
                                    </tr>
                                    </thead>

                                    <tbody>
                                    {sortedClients.map((client, index) => (
                                        <tr key={index}>
                                            <td>{client.Surname}</td>
                                            <td>{client.CreditScore}</td>
                                            <td>{translateCountry(client.Geography)}</td>
                                            <td>
                                <span className={
                                    client.Gender === "Male"
                                        ? styles.genderMale
                                        : styles.genderFemale
                                }>
                                    {translateGender(client.Gender)}
                                </span>
                                            </td>
                                            <td>{client.Age}</td>
                                            <td>{client.Tenure}</td>
                                            <td>{Math.round(client.Balance).toLocaleString("ru-RU")}</td>
                                            <td>{client.NumOfProducts}</td>
                                            <td>{client.HasCrCard ? "Да" : "Нет"}</td>
                                            <td>{client.IsActiveMember ? "Да" : "Нет"}</td>
                                            <td>{Math.round(client.EstimatedSalary).toLocaleString("ru-RU")}</td>
                                            <td className={styles.churnCell}>
                                                {(client.ChurnProbability * 100).toFixed(1)}%
                                            </td>
                                        </tr>
                                    ))}
                                    </tbody>
                                </table>
                            </div>
                        </>
                    )
                )}


            </div>
        </>
    );
}
