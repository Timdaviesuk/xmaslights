async function light(channel, signal) {
    const url = `api/light/${channel}?signal=${signal}`;
    // const url = `http://192.168.178.51:2801/api/light/${channel}?signal=${signal}`;
    const response = await fetch(url);
    console.log(response);
}