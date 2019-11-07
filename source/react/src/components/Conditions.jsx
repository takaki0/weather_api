import React from 'react';
import PropTypes from 'prop-types';

import Condition from './Condition';


const Conditions = ({ conditions, city_name }) => (
  <div>
    <h3>気象検索結果:{city_name}</h3>
    <table>
      <thead>
        <tr>
          <th width="120px">日付</th>
          <th width="100px">最高気温</th>
          <th width="100px">最低気温</th>
          <th width="100px">雲量</th>
          <th width="100px">湿度</th>
          <th width="100px">降水確率</th>
          <th width="100px">気圧</th>
          <th width="100px">オゾン指数</th>
        </tr>
      </thead>
      <tbody>
        {conditions.map(condition => (<Condition key={condition.date} condition={condition} />))}
      </tbody>
    </table>
  </div>
);

Conditions.propTypes = {
  conditions: PropTypes.arrayOf(PropTypes.any),
  city_name: PropTypes.string,
};

Conditions.defaultProps = {
  conditions: [],
  city_name: '',
};

export default Conditions;
