const nunjucks = require('nunjucks');
const puppeteer = require('puppeteer');
const { PubSub } = require('@google-cloud/pubsub');

exports.generateImage = async function (html = "") {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.setContent(html);

  const content = await page.$("body");
  const imageBuffer = await content.screenshot({ omitBackground: true });

  await page.close();
  await browser.close();

  return imageBuffer;
};

async function publishMessage(
  projectId = 'archy-f06ed',
  topicName = 'channel_message_discord',
  payloadData
) {
  const pubsub = new PubSub({ projectId });

  const dataBuffer = Buffer.from(JSON.stringify(payloadData));
  const messageId = await pubsub.topic(topicName).publish(dataBuffer);
  conso.log(`Message ${messageId} published.`);

  return messageId;
}

exports.generateWelcomeImage = async (event, context) => {
  const data = event.data
    ? Buffer.from(event.data, 'base64').toString()
    : undefined;

  if (data === undefined) {
    throw SyntaxError;
  }

  const payload = JSON.parse(data).payload;
  const channelId = JSON.parse(data).channel_id;

  nunjucks.configure({ autoescape: true });

  let html = nunjucks.render('./templates/welcome.html', {
    username: payload.username,
    avatar_url: payload.avatar_url,
  });

  const imageBuffer = await this.generateImage(html);

  const messageData = { "channel_id": channelId, "image": imageBuffer.toString('base64') }

  await publishMessage(
    projectId = 'archy-f06ed',
    topicName = 'channel_message_discord',
    payloadData = messageData
  );

};
