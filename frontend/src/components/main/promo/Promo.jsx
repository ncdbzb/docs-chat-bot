import { Link } from 'react-router-dom';
import './promo.css'

const Header = () =>{
    return (
        <section className="main-container">
            <div className="promo-info">
                <h2>AI-ассистент для работы с документацией</h2>
                <p>
                    Он может:
                </p>
                <ul>
                    <li>Генерировать тестовые вопросы</li>
                    <li>Отвечать на вопросы по содержанию документа</li>
                </ul>
            </div>
        </section>
    );
}

export default Header;