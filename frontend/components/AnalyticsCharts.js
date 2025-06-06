import {
    Bar,
} from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend
} from "chart.js";
import styles from "@/styles/Analytics.module.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const CHART_COLORS = [
    "#CDB4DB",
    "#FFC8DD",
    "#FFAFCC",
    "#BDE0FE",
    "#A2D2FF"
];

export default function AnalyticsCharts({ data }) {
    const createBarData = (dataset, label) => ({
        labels: Object.keys(dataset),
        datasets: [
            {
                label,
                data: Object.values(dataset).map(v => (v * 100).toFixed(1)),
                backgroundColor: CHART_COLORS,
                borderRadius: 8,
            },
        ],
    });

    const commonOptions = {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: ctx => `${ctx.raw}%`,
                },
            },
        },
        scales: {
            y: { beginAtZero: true, ticks: { callback: val => `${val}%` } },
        },
    };

    return (
        <div className={styles.chartGrid}>
            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по возрасту</h3>
                <Bar data={createBarData(data.age_groups, "Возраст")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по полу</h3>
                <Bar data={createBarData(data.gender, "Пол")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по странам</h3>
                <Bar data={createBarData(data.geography, "Страна")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по кредитному рейтингу</h3>
                <Bar data={createBarData(data.credit_score, "Кредитный рейтинг")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по балансу на счету</h3>
                <Bar data={createBarData(data.balance, "Баланс")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по оценочной зарплате</h3>
                <Bar data={createBarData(data.estimated_salary, "Зарплата")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по активности клиента</h3>
                <Bar data={createBarData(data.activity, "Активность")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по стажу</h3>
                <Bar data={createBarData(data.tenure, "Стаж")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по кол-ву продуктов</h3>
                <Bar data={createBarData(data.num_of_products, "Продукты")} options={commonOptions} />
            </div>

            <div className={styles.chartBlock}>
                <h3 style={{ color: "#CD9EE8" }}>Вероятность оттока по кредитной карте</h3>
                <Bar data={createBarData(data.has_credit_card, "Кредитка")} options={commonOptions} />
            </div>
        </div>
    );
}
