import {useState, useEffect} from "react";
import {useRouter} from "next/router";
import Header from "@/components/header";
import styles from "@/styles/Analytics.module.css";
import AnalyticsCharts from "@/components/AnalyticsCharts";

export default function Analytics() {
    const router = useRouter();
    const [view, setView] = useState("analytics");
    const [clientsInfo, setClientsInfo] = useState([]);
    const [analyticsData, setAnalyticsData] = useState(null);

    useEffect(() => {
        if (router.query.data) {
            try {
                const parsed = JSON.parse(router.query.data);
                setClientsInfo(parsed.clients_info);
                setAnalyticsData(parsed.analytics); // добавлено
            } catch (err) {
                console.error("Ошибка парсинга данных:", err);
            }
        }
    }, [router.query]);

    const tableHeaders = [
        "Фамилия",
        "Кредитный рейтинг",
        "Страна",
        "Пол",
        "Возраст",
        "Стаж",
        "Баланс",
        "Кол-во продуктов",
        "Кредитная карта",
        "Активный клиент",
        "Оценочная зарплата",
        "Вероятность оттока"
    ];

    const translateCountry = (country) => {
        switch (country) {
            case "Germany":
                return "Германия";
            case "France":
                return "Франция";
            case "Spain":
                return "Испания";
            default:
                return country;
        }
    };

    const translateGender = (gender) =>
        gender === "Male" ? "Мужской" : "Женский";

    return (
        <>
            <Header/>
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


                {view === "analytics" && analyticsData && (
                    <AnalyticsCharts data={analyticsData} />
                )}

                {view === "top" && (
                    <div style={{overflowX: "auto"}}>
                        <table className={styles.table}>
                            <thead>
                            <tr>
                                {tableHeaders.map((header, index) => (
                                    <th key={index}>{header}</th>
                                ))}
                            </tr>
                            </thead>
                            <tbody>
                            {clientsInfo.map((client, index) => (
                                <tr key={index}>
                                    <td>{client.Surname}</td>
                                    <td>{client.CreditScore}</td>
                                    <td>{translateCountry(client.Geography)}</td>
                                    <td>
                      <span className={
                          client.Gender === "Male" ? styles.genderMale : styles.genderFemale
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
                )}
            </div>
        </>
    );
}
