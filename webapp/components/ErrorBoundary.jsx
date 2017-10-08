import React, {Component} from 'react';
import idx from 'idx';
// This is being pulled form the CDN currently
// import Raven from 'raven-js';

import IdentityNeedsUpgradeError from './IdentityNeedsUpgradeError';
import InternalError from './InternalError';
import Login from './Login';
import NotFoundError from './NotFoundError';
import {Error401, Error404} from '../errors';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = {error: null};
  }

  unstable_handleError(...params) {
    // This method is a fallback for react <= 16.0.0-alpha.13
    this.componentDidError(...params);
  }

  componentDidCatch(error, errorInfo) {
    this.setState({error});
    if (error.constructor === Error && window.Raven) {
      window.Raven.captureException(error, {extra: errorInfo});
      window.Raven.lastEventId() && window.Raven.showReportDialog();
    }
  }

  render() {
    let {error} = this.state;
    if (error) {
      switch (error.constructor) {
        case Error404:
          return <NotFoundError />;
        case Error401:
          if (idx(error, _ => _.data.error) === 'identity_needs_upgrade') {
            return <IdentityNeedsUpgradeError url={error.data.url} />;
          }
          // XXX(dcramer): this works around the issue where an identity has
          // been removed
          return <Login />;
        default:
          return <InternalError error={error} />;
      }
    } else {
      return this.props.children;
    }
  }
}
