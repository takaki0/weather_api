import React, { Component } from 'react';
import PropTypes from 'prop-types';


class SearchForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      city_name: '東京',
      from_date: '2019-11-01',
      to_date: '2019-11-03',
    };
  }

  // eslint-disable-next-line camelcase
  handlePlaceChange(city_name) {
    this.setState({ city_name });
  }

  // eslint-disable-next-line camelcase
  handleFromDateChange(from_date) {
    this.setState({ from_date });
  }

  // eslint-disable-next-line camelcase
  handleToDateChange(to_date) {
    this.setState({ to_date });
  }

  handleSubmit(event) {
    event.preventDefault();
    this.props.onSubmit(this.state.city_name, this.state.from_date, this.state.to_date);
  }

  render() {
    return (
      <form className="search-form" onSubmit={event => this.handleSubmit(event)}>
        都市：
        <input
          className="place-input"
          type="text"
          value={this.state.city_name}
          onChange={event => this.handlePlaceChange(event.target.value)}
        />
        期間（開始日）：
        <input
          className="date-input"
          type="text"
          value={this.state.from_date}
          onChange={event => this.handleFromDateChange(event.target.value)}
        />
        〜（終了日）：
        <input
          className="date-input"
          type="text"
          value={this.state.to_date}
          onChange={event => this.handleToDateChange(event.target.value)}
        />
        <input className="submit-button" type="submit" value="検索" />
      </form>
    );
  }
}

SearchForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
};

export default SearchForm;
