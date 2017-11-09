import React from 'react';
import {connect} from 'react-redux';
import styled from 'styled-components';

import {addIndicator, removeIndicator} from '../actions/indicators';
import AsyncPage from '../components/AsyncPage';
import Button from '../components/Button';
import SectionHeading from '../components/SectionHeading';

const WarningMessage = styled.span`
  color: #e03e2f;
  margin-left: 1em;
`;

class TokenSettings extends AsyncPage {
  getEndpoints() {
    return [['token', '/user/token']];
  }

  renewToken = async () => {
    try {
      const token = await this.api.post('/user/token');
      this.setState({token});
    } catch (e) {
      this.props.addIndicator('Could not create a new token.', 'error', 5000);
    }
  };

  renderBody() {
    const {token} = this.state;
    return token ? (
      <div>
        <SectionHeading>This is your API token:</SectionHeading>
        <pre>zeus-u-{token.key}</pre>
        <Button type="danger" onClick={this.renewToken}>
          Refresh API Token
        </Button>
        <WarningMessage>The old token will be invalid afterwards</WarningMessage>
      </div>
    ) : (
      <div>
        <SectionHeading>You have not createt an API token yet</SectionHeading>
        <pre>zeus-u-{token.key}</pre>
        <Button onClick={this.renewToken}>Generate API Token</Button>
      </div>
    );
  }
}

export default connect(null, {
  addIndicator,
  removeIndicator
})(TokenSettings);
