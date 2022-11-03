import { ImageResponse } from "@vercel/og";
import { NextRequest } from "next/server";

// http://localhost:3000/api/bar?username=Hannibal119&rank=540&level=62&avatar_url=135048445097410560%2Fc71476c9a123cb79d1859687792bf9c3&exp_toward_next_level=432&level_exp_needed=1000

export const config = {
  runtime: "experimental-edge",
};

function kFormatter(num: number) {
  return Math.abs(num) > 999
    ? Math.sign(num) * +(Math.abs(num) / 1000).toFixed(1) + "k"
    : Math.sign(num) * Math.abs(num);
}

export default function handler(req: NextRequest) {
  try {
    const searchParams = new URLSearchParams(req.nextUrl.search);

    const hasUsername = searchParams.has("username");
    const username = hasUsername
      ? searchParams.get("username")
      : "Who are you?";

    const hasAvatarUrl = searchParams.has("avatar_url");
    const avatarUrl = hasAvatarUrl ? searchParams.get("avatar_url") : "...";

    const hasRank = searchParams.has("rank");
    const rank = hasRank ? searchParams.get("rank") : "999";

    const hasLevel = searchParams.has("level");
    const level = hasLevel ? searchParams.get("level") : "0";

    const hasExp = searchParams.has("exp_toward_next_level");
    const exp = hasExp ? searchParams.get("exp_toward_next_level") : "0";

    const hasExpNeeded = searchParams.has("level_exp_needed");
    const expNeeded = hasExpNeeded ? searchParams.get("level_exp_needed") : "0";

    let percent = (+exp! / +expNeeded!) * 100;
    let percentValue = +percent! > 6 ? percent : 6;

    const expFormatted = kFormatter(+exp!);
    const expNeededFormatted = kFormatter(+expNeeded!);

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
                justifyContent: "flex-start",
                alignItems: "flex-start",
                flex: 1,
              }}
            >
              <div
                style={{
                  display: "flex",
                  margin: "auto 0",
                  height: "100%",
                  width: "100%",
                  // background: "red"
                }}
              >
                <img
                  style={{
                    margin: "auto",
                    width: "340px",
                    height: "340px",
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
                justifyContent: "space-between",
                height: "100%",
                flex: 3,
                marginLeft: "40px",
              }}
            >
              <img
                style={{
                  position: "absolute",
                  top: "10px",
                  left: "10px",
                  width: "200px",
                  height: "200px",
                  borderRadius: "25px",
                  opacity: "0.3",
                }}
                src="https://cdn.discordapp.com/emojis/1022875335697629246.png"
              />

              <div
                style={{
                  display: "flex",
                  width: "100%",
                  justifyContent: "flex-end",
                  margin: "40px 0",
                  fontSize: "40px",
                }}
              >
                <div style={{ display: "flex" }}>
                  <span
                    style={{
                      display: "flex",
                      alignItems: "flex-end",
                      height: "120px",
                      color: "grey",
                    }}
                  >
                    Rank
                  </span>
                  <span
                    style={{
                      marginLeft: "20px",
                      fontSize: "100px",
                    }}
                  >
                    # {rank}
                  </span>
                </div>
                <span
                  style={{
                    marginLeft: "20px",
                    display: "flex",
                    alignItems: "flex-end",
                    height: "120px",
                    color: "grey",
                  }}
                >
                  Level
                </span>
                <span
                  style={{
                    marginLeft: "10px",
                    fontSize: "100px",
                  }}
                >
                  {level}
                </span>
              </div>
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  width: "100%",

                  fontSize: "50px",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    width: "100%",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ display: "flex" }}>
                    <span>{username}</span>
                    <span style={{ color: "grey", marginLeft: "10px" }}>
                      {/* #2356 */}
                    </span>
                  </div>
                  <div style={{ display: "flex" }}>
                    <span>{expFormatted}</span>
                    <span style={{ color: "grey", marginLeft: "10px" }}>
                      / {expNeededFormatted}
                    </span>
                  </div>
                </div>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "flex-end",
                    height: "50px",
                    width: "100%",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      height: "50px",
                      width: "100%",
                      borderRadius: "25px",
                      background: "rgb(217, 217, 217)",
                    }}
                  >
                    <div
                      style={{
                        width: `${percentValue}%`,
                        height: "100%",
                        background: "rgb(58, 183, 1)",

                        borderRadius: "25px",
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      ),
      {
        width: 1400,
        height: 500,
      }
    );
  } catch (e: any) {
    console.log(`${e.message}`);
    return new Response(`Failed to generate the image`, {
      status: 500,
    });
  }
}
