import React from 'react';
import PropTypes from 'prop-types';


const Condition = ({ condition }) => (
  <tr>
    <td>{condition.date}</td>
    <td>{condition.temperatureMax}</td>
    <td>{condition.temperatureMin}</td>
    <td>{condition.cloudCover}</td>
    <td>{condition.humidity}</td>
    <td>{condition.precipProbability}</td>
    <td>{condition.pressure}</td>
    <td>{condition.ozone}</td>
  </tr>
);

Condition.propTypes = {
  condition: PropTypes.shape({
    date: PropTypes.string,
    temperatureMax: PropTypes.number,
    temperatureMin: PropTypes.number,
    cloudCover: PropTypes.number,
    humidity: PropTypes.number,
    precipProbability: PropTypes.number,
    pressure: PropTypes.number,
    ozone: PropTypes.number,
  }).isRequired,
};

export default Condition;
