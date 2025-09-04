import { Link } from 'react-router-dom';
import './promo.css'

const Header = () => {
    return (
        <section className="main-container">
            <div className="promo-info">
                <h2 className="promo-title">AI-ассистент для работы с документацией</h2>
                
                <p className="promo-text">
                    Загружайте свои документы и получайте быстрый доступ к знаниям, содержащимся в них. 
                    Наш AI-ассистент помогает изучать материалы эффективнее и удобнее.
                </p>

                <p className="promo-text">
                    Сервис предоставляет две основные функции:
                </p>

                <ul className="promo-list">
                    <li>
                        <strong>Ответы на вопросы по документу:</strong> задайте вопрос о содержании загруженного документа, 
                        и система предоставит точный ответ, опираясь на текст документа.
                    </li>
                    <li>
                        <strong>Генерация тестовых вопросов:</strong> AI создаст тест с четырьмя вариантами ответа, 
                        вы сможете выбрать один из них и сразу увидеть, правильно ли вы ответили. 
                        Это отличный способ проверить свои знания и закрепить материал.
                    </li>
                </ul>

                <p className="promo-text">
                    Наш ассистент помогает экономить время, улучшать понимание документации и эффективно готовиться к проверке знаний.
                </p>
            </div>

            <style jsx>{`
                .promo-info {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 2rem;
                    line-height: 1.6;
                    font-size: 1rem;
                    color: #333;
                }

                .promo-title {
                    font-size: 2rem;
                    margin-bottom: 1.5rem;
                    text-align: center;
                }

                .promo-text {
                    margin-bottom: 1.2rem;
                }

                .promo-list {
                    list-style: disc;
                    margin-left: 2rem;
                    margin-bottom: 1.5rem;
                }

                .promo-list li {
                    margin-bottom: 0.8rem;
                }
            `}</style>
        </section>
    );
}



export default Header;