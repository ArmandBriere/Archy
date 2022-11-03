import { ImageResponse } from "@vercel/og";
import { NextRequest } from "next/server";

// http://localhost:3000/api/circle?username=Hannibal119&adjectif=wow&rank=1&level=62&percent=33&avatarUrl=135048445097410560%2Fc71476c9a123cb79d1859687792bf9c3

export const config = {
  runtime: "experimental-edge",
};

export default function handler(req: NextRequest) {
  try {
    const searchParams = new URLSearchParams(req.nextUrl.search);
    console.log(req.nextUrl.search);
    console.log(searchParams);
    const hasUsername = searchParams.has("username");
    const username = hasUsername
      ? searchParams.get("username")
      : "Who are you?";

    const hasAdjectif = searchParams.has("adjectif");
    const adjectif = hasAdjectif ? searchParams.get("adjectif") : "...";

    const hasAvatarUrl = searchParams.has("avatarUrl");
    const avatarUrl = hasAvatarUrl ? searchParams.get("avatarUrl") : "...";

    const hasRank = searchParams.has("rank");
    const rank = hasRank ? searchParams.get("rank") : "-999";

    const hasLevel = searchParams.has("level");
    const level = hasLevel ? searchParams.get("level") : "-999";

    const hasPercent = searchParams.has("percent");
    const percent = hasPercent ? searchParams.get("percent") : "0";

    console.log(username);
    console.log(adjectif);
    console.log(avatarUrl);
    console.log(rank);
    console.log(level);
    console.log(percent);
    return new ImageResponse(
      (
        <div
          style={{
            boxSizing: "border-box",
            padding: "80px",
            width: "100%",
            height: "100%",

            borderRadius: "20px",
            background: "rgb(32, 48, 24)",

            display: "flex",
            flexDirection: "column",
            justifyContent: "center",

            color: "white",
          }}
        >
          <div
            style={{
              fontSize: "80px",
              overflowX: "clip",
              textAlign: "center",
              margin: "-20px auto 40px auto",
              padding: "-20px 80px 80px 80px",
            }}
          >
            {username}
          </div>

          <div
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "space-around",
              width: "100%",
            }}
          >
            {/* User */}
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                flex: 1,
              }}
            >
              <div
                style={{
                  marginBottom: "40px",
                  fontSize: "40px",
                  overflowX: "clip",
                }}
              >
                {adjectif}
              </div>
              <div
                style={{
                  display: "flex",

                  justifyContent: "center",
                  alignItems: "center",
                  height: "400px",
                }}
              >
                <img
                  style={{
                    position: "absolute",
                    width: "400px",
                    height: "400px",
                    borderRadius: "50%",
                  }}
                  src={`http://cdn.discordapp.com/avatars/${avatarUrl}.png`}
                />
              </div>
            </div>

            {/* Rank */}
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                flex: 1,
              }}
            >
              <div
                style={{
                  marginBottom: "40px",
                  fontSize: "40px",
                  overflowX: "clip",
                }}
              >
                Rank
              </div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  height: "400px",
                }}
              >
                <p
                  style={{
                    zIndex: "100",
                    textAlign: "center",
                    margin: "auto",
                    fontSize: "80px",
                    alignContent: "center",
                  }}
                >
                  {rank}
                </p>
                <img
                  style={{
                    position: "absolute",
                    width: "400px",
                    height: "400px",
                    borderRadius: "25px",
                    opacity: "0.3",
                  }}
                  src="https://cdn.discordapp.com/emojis/1022875335697629246.png"
                />
              </div>
            </div>

            {/* Level */}
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                flex: 1,
              }}
            >
              <div
                style={{
                  display: "flex",
                  marginBottom: "40px",
                  overflowX: "clip",
                  fontSize: "40px",
                  alignContent: "center",
                  textAlign: "center",
                }}
              >
                Level {level}
              </div>
              <div
                style={{
                  display: "flex",
                  position: "relative",
                  borderRadius: "50%",
                  width: "400px",
                  height: "400px",
                  backgroundColor: "rgb(217, 217, 217)",
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    padding: "50px",
                    margin: "50px",
                    borderRadius: "50%",
                    width: "300px",
                    height: "300px",
                    background: "rgb(32, 48, 24)",
                  }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      ),
      {
        width: 1680,
        height: 720,
      }
    );
  } catch (e: any) {
    console.log(`${e.message}`);
    return new Response(`Failed to generate the image`, {
      status: 500,
    });
  }
}
