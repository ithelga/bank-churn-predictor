import React, {useContext, useEffect, useState} from 'react';
import styles from "@/styles/header.module.css";
import {useRouter} from 'next/router';


const Header = () => {
    const router = useRouter();
    const [activePage, setActivePage] = useState('bond');

    
    useEffect(() => {
        const path = router.pathname.split('/')[1];
        setActivePage(path || '/');
    }, [router.pathname]);


    const handleNavigation = (page) => {
            setActivePage(page);
            if (page == '/' ) router.push(`/${page}`)
    };


    return (
        <div className={styles.container}>
            <header className={styles.header}>

                <div className={styles.logoContainer}>
                    <img 
                        src="/logo.png" 
                        alt="Icon" 
                        className={styles.iconLogo} 
                        onClick={() => handleNavigation('/')} 
                    />
                    <div className={styles.textContainer}>
                        <span className={styles.title}>Лояльность 2.0</span>
                        <span className={styles.subtitle}>Сервис прогнозирования оттока клиентов</span>
                    </div>
                </div>
            </header>

          

            <div className={styles.line}></div>
        </div>
    );
};

export default Header;
