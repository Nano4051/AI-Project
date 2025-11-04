import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/video-data")
      .then(res => res.json())
      .then(data => setData(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>WalkVideo 프로젝트</h1>
      {data ? (
        <p>📹 프레임 수: {data.frame_count}, 상태: {data.status}</p>
      ) : (
        <p>로딩 중...</p>
      )}
    </div>
  );
}

export default App;
