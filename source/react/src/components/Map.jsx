import React from 'react';
import { withGoogleMap, GoogleMap, Marker } from 'react-google-maps';
import PropTypes from 'prop-types';

const InnerMap = withGoogleMap(props => (
  <GoogleMap
    ref={props.onMapLoad}
    defaultZoom={8}
    defaultCenter={props.position}
    center={props.position}
  >
    <Marker {...props.marker} />
  </GoogleMap>
));

const Map = ({ location }) => {
  const position = location;
  return (<InnerMap
    containerElement={(<div />)}
    mapElement={(<div className="map" />)}
    position={position}
    marker={{ position }}
  />);
};

Map.propTypes = {
  location: PropTypes.objectOf(PropTypes.number).isRequired,
};


export default Map;
