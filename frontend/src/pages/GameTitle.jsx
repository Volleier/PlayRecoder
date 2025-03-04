import React, { useEffect, useState } from 'react';
import axios from 'axios';

const GamesTable = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get('http://127.0.0.1:5000/api/games/123456789');  // 替换为真实 Steam ID
      setGames(response.data.response.games);
    };
    fetchData();
  }, []);

  return (
    <div>
      <h2>Games Table</h2>
      <table>
        <thead>
          <tr>
            <th>Game Name</th>
            <th>Playtime (hours)</th>
          </tr>
        </thead>
        <tbody>
          {games.map((game) => (
            <tr key={game.appid}>
              <td>{game.name}</td>
              <td>{Math.floor(game.playtime_forever / 60)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default GamesTable;