export default function VideoFeed({ running }) {
  if (!running) {
    return (
      <div style={placeholderStyle}>
        <p>Proctoring not started</p>
      </div>
    );
  }

  return (
    <img
      src="http://127.0.0.1:5000/video"
      alt="Live Proctoring Feed"
      style={videoStyle}
    />
  );
}

const videoStyle = {
  width: "100%",
  borderRadius: "10px",
  border: "2px solid #334155"
};

const placeholderStyle = {
  height: "360px",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  background: "#020617",
  borderRadius: "10px",
  color: "#94a3b8",
  border: "2px dashed #334155"
};
