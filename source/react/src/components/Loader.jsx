import React from 'react';
import PropTypes from 'prop-types';

const Loader = ({ loading }) => {
  if (loading === true) {
    return (<div id="loading"><div className="loadingMsg">処理中です...</div></div>);
  }
  return null;
};

Loader.propTypes = {
  loading: PropTypes.bool.isRequired,
};

export default Loader;

