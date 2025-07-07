import { Link } from 'react-router-dom';
import './promo.css'

const Header = () =>{
    return (
        <section class="main-container">
            <Link className='link-leaderboard' to={`leaderboard/DATAPK_VERSION_2_1`}>Рейтинг по документации DATAPK_VERSION_2_1</Link>
            <Link className='link-leaderboard' to={`leaderboard/DATAPK_ITM_VERSION_1_7`}>Рейтинг по документации DATAPK_ITM_VERSION_1_7</Link>
        </section>
    );
}

export default Header;