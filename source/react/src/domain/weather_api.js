import Axios from 'axios';

const WEATHER_API_ENDPOINT = '/weather/get_condition_by_city/dc5c49bc74131f57699d93c3e961d86a';

// eslint-disable-next-line camelcase
export const weatherApi = (city_name, from_date, to_date) =>
  // Axios.get(WEATHER_API_ENDPOINT}?city_name=Paris&from_date=${from_date}&to_date=${to_date}`)
  Axios.get(WEATHER_API_ENDPOINT, { params: { city_name, from_date, to_date } })
    .then((result) => {
      console.log(result);
      const status = result.data.status;
      const message = result.data.message;
      if (status !== 200) {
        return { status, message };
      }

      const conditions = result.data.weather_conditions;
      const latlng = result.data.location;
      const location = { lat: latlng.latitude, lng: latlng.longitude };
      return { status, message, conditions, location };
    })
    .catch((error) => {
      console.log('catch!!');
      console.log(error);
      const status = 500;
      const message = 'url error';
      return { status, message };
    });


export const otherMethod = () => null;

