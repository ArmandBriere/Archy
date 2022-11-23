import { ImageResponse } from "@vercel/og";
import { NextRequest } from "next/server";

// http://localhost:3000/api/bar?username=Hannibal119&avatar_url=135048445097410560%2Fc71476c9a123cb79d1859687792bf9c3&rank=1&level=62&exp_toward_next_level=33&level_exp_needed=550&exp=10

export const config = {
  runtime: "experimental-edge",
};

function kFormatter(num: number): string {
  // Format a number into a string with k
  return Math.abs(num) > 999
    ? Math.sign(num) * +(Math.abs(num) / 1000).toFixed(1) + "k"
    : Math.sign(num) * Math.abs(num) + "";
}

function getRandomFroge(): String {
  const froges = [
    "bonkfroge.png",
    "froge.png",
    "frogeangry.png",
    "frogeangryshaking.gif",
    "frogebonk.png",
    "frogechicken.gif",
    "frogedetective.png",
    "frogefr.png",
    "frogehacker.png",
    "frogeheart.png",
    "frogeking.png",
    "frogelove.png",
    "frogeparty.png",
    "frogepeek.png",
    "frogepopcorn.gif",
    "frogepopcorn.png",
    "frogepuke.png",
    "frogesad.png",
    "frogeshh.png",
    "frogesilly.gif",
    "frogesip.png",
    "frogesith.png",
    "frogesleep.png",
    "frogesmile.png",
    "frogestonks.png",
    "frogestudy.png",
    "frogesuspicious.png",
    "frogethink.png",
    "frogeyoda.png",
    "lovefroge.png",
    "noodlefroge.png",
    "partyfroge.png",
    "policefroge.png",
    "popcornfroge.png",
    "popefroge.png",
    "thinkfroge.png",
    "yodafroge.png",
  ];

  return froges[Math.floor(Math.random() * froges.length)];
}

export default function handler(req: NextRequest) {
  // Handle the http requests.
  // Generates the image
  try {
    const searchParams = new URLSearchParams(req.nextUrl.search);

    const hasUsername = searchParams.has("username");
    const username = hasUsername ? searchParams.get("username") : undefined;

    const hasAvatarUrl = searchParams.has("avatar_url");
    const avatarUrl = hasAvatarUrl ? searchParams.get("avatar_url") : undefined;

    const hasRank = searchParams.has("rank");
    const rank = hasRank ? searchParams.get("rank") : undefined;

    const hasLevel = searchParams.has("level");
    const level = hasLevel ? searchParams.get("level") : undefined;

    const hasExp = searchParams.has("exp_toward_next_level");
    const exp = hasExp ? searchParams.get("exp_toward_next_level") : undefined;

    const hasExpNeeded = searchParams.has("level_exp_needed");
    const expNeeded = hasExpNeeded
      ? searchParams.get("level_exp_needed")
      : undefined;

    if (
      [username, avatarUrl, rank, level, exp, expNeeded].includes(undefined)
    ) {
      throw Error("Missing parameters");
    }

    let percent = (+exp! / +expNeeded!) * 100;
    let percentValue = +percent! > 6 ? percent : 6;

    const expFormatted = kFormatter(+exp!);
    const expNeededFormatted = kFormatter(+expNeeded!);

    let randomFroge = `https://storage.googleapis.com/froge-bucket-prod/${getRandomFroge()}`;

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
                src={`${randomFroge}`}
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
    return new ImageResponse(
      (
        <div style={{ display: "flex", background: "transparent" }}>
          <img src="https://storage.googleapis.com/froge-bucket-prod/archy.jpg" />
        </div>
      ),
      { width: 448, height: 448 }
    );
  }
}
