import React, { Component } from 'react';

import SearchForm from './SearchForm';
import Conditions from './Conditions';
import Map from './Map';

import { weatherApi } from '../domain/weather_api';
import Loader from './Loader';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      city_name: '東京',
      location: {
        lat: 35.6585805,
        lng: 139.7454329,
      },
      from_date: '2019-11-01',
      to_date: '2019-11-05',
      conditions: [],
      loading: false,
    };
  }

  // eslint-disable-next-line class-methods-use-this,camelcase
  handlePlaceSubmit(city_name, from_date, to_date) {
    console.log(city_name);
    console.log(from_date);
    console.log(to_date);
    this.setState({ city_name, from_date, to_date, loading: true });
    weatherApi(city_name, from_date, to_date)
      .then(({ status, message, conditions, location }) => {
        switch (status) {
          case 200: {
            this.setState({
              location,
              conditions,
              loading: false,
            });
            console.log(this.state);
            console.log(this.state.conditions[0].temperatureMax);
            console.log(this.state.conditions[0].temperatureMin);
            break;
          }
          case 401: {
            console.log(message);
            break;
          }
          case 500: {
            console.log(message);
            break;
          }
          default: {
            console.log(message);
            break;
          }
        }
      });
  }

  render() {
    return (
      <div className="app">
        <h1>気象情報検索　2.</h1>
        {/* eslint-disable-next-line react/jsx-no-target-blank */}
        <h4>
          <a
            href="https://github.com/takaki0/weather_api"
            target="_blank"
            rel="noopener noreferrer"
          >
            github URLはコチラ: https://github.com/takaki0/weather_api
          </a>
        </h4>
        <SearchForm
          onSubmit={(city_name, from_date, to_date) =>
            this.handlePlaceSubmit(city_name, from_date, to_date)}
        />
        <div className="result">
          <Map location={this.state.location} />
          <Conditions conditions={this.state.conditions} city_name={this.state.city_name} />
        </div>
        <Loader loading={this.state.loading} />
      </div>
    );
  }

}


export default App;

