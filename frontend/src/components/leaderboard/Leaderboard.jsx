import React from 'react';
import { useRequastLeaderboard } from "./requestLeaderboard";
import './leaderboard.css';

function Leaderboard({ data }) {
  const { userData, isLoggedIn } = useRequastLeaderboard(data);
  if (!isLoggedIn || !userData.length) {
    return <h1>Ещё никто не участвовал</h1>;
  }

  return (
    <section className='leaderboard_page'>
      <div className="container_leaderboard">

        <h1>Рейтинг по документации {data}</h1>
        <table className="table-leaderboard">
          <thead>
            <tr>
              <th>Место</th>
              <th>Фамилия</th>
              <th>Имя</th>
              <th>Кол-во пройденных тестов</th>
              <th>Кол-во очков</th>
            </tr>
          </thead>
          <tbody>
            {userData.map((item) => (
              <tr key={item.id}>
                <td>{item.place}</td>
                <td>{item.surname}</td>
                <td>{item.name}</td>
                <td>{item.total_tests}</td>
                <td>{item.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default Leaderboard;