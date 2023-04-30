const getNotificationsApi = async () => {
  try {
    const response = await fetch("http://localhost:8000/notification", {
      method: "get",
    });
    const result = await response.json();

    return result;
  } catch (err) {
    console.log(err);
  }
};

export default getNotificationsApi;
