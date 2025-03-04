import React, { useEffect, useState } from "react";
import "./App.css"; // Import styles

const App: React.FC = () => {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  useEffect(() => {
    // Get today's date in local time zone (MM-DD format)
    const today = new Intl.DateTimeFormat("en-CA", {
      month: "2-digit",
      day: "2-digit",
    })
      .format(new Date())
      .replace("/", "-");

    const fetchVideo = async () => {
      try {
        const response = await fetch(`${process.env.PUBLIC_URL}/videos.json`);
        const videoData = await response.json();
        if (videoData[today]) {
          const videos: string[] = videoData[today];
          const randomVideoUrl =
            videos[Math.floor(Math.random() * videos.length)];
          setVideoUrl(randomVideoUrl);
        } else {
          setVideoUrl(null);
        }
      } catch (error) {
        console.error("❌ Error fetching videos.json:", error);
        setVideoUrl(null);
      }
    };

    fetchVideo();
  }, []);

  return (
    <div className="theater-container">
      {/* Lynchian Red Curtains */}
      <div className="curtain curtain-left"></div>
      <div className="curtain curtain-right"></div>

      <h1 className="theater-title">THE WEATHER</h1>

      {/* TV Stand with Wooden Frame */}
      <div className="tv-container glitch">
        {/* TV Frame */}
        <div className="tv-frame">
          {/* TV Screen */}
          <div className="tv-screen crt">
            {videoUrl ? (
              <iframe
                src={videoUrl}
                title="Today's Video"
                allowFullScreen
                className="youtube-iframe"
              ></iframe>
            ) : (
              <p>No video available for today.</p>
            )}
          </div>

          {/* TV Knobs */}
          <div className="tv-knobs">
            <div className="knob red"></div>
            <div className="knob green"></div>
            <div className="knob yellow"></div>
          </div>
        </div>

        {/* Wooden Legs */}
        <div className="tv-legs">
          <div className="leg left"></div>
          <div className="leg right"></div>
        </div>
      </div>
    </div>
  );
};

export default App;
