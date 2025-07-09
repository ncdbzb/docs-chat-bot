import React from "react";
import { useRequestLeaderboardMe } from "./requestLeaderboardMe";
import { Link } from 'react-router-dom';

const Leaderboard = () => {
  const { userData, isLoading } = useRequestLeaderboardMe();

  if (isLoading) {
    return <div>Загрузка данных...</div>;
  }

  // Преобразование userData в массив
  const leaderboardData = Object.values(userData).map(({ doc_name, leaderboard }) => ({
    doc_name,
    leaderboard,
  }));

  return (
    <>
      {leaderboardData.map(({ doc_name, leaderboard }, index) => (
        leaderboard.length > 0 && (
          <div key={index} className="container_leaderboard">
            <h2>Рейтинг по документации {doc_name}</h2>
            {/* Отображение таблицы с данными лидерборда */}
            <table className="table-leaderboard">
              <thead>
                <tr>
                  <th>Место</th>
                  <th>Имя</th>
                  <th>Очки</th>
                  <th>Пройдено</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((participant, idx) => (
                  <tr key={idx}>
                    <td>{participant.place}</td>
                    <td>{participant.surname} {participant.name}</td>
                    <td>{participant.points}</td>
                    <td>{participant.total_tests}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <Link className='link-leaderboard' to={`/leaderboard/${doc_name}`}>Полный рейтинг</Link>
          </div>
        )
      ))}
    </>
  );
};

export default Leaderboard;
