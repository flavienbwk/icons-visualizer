import React from 'react';
import { HashRouter as Router, Route } from 'react-router-dom';
import Home from './Home';
import { About } from './About';
import { Layout } from './Layout';
import { NavigationBar } from './NavigationBar';

function App() {

    return (
        <React.Fragment>
            <Router>
                <NavigationBar />
                <Layout>
                    <Route exact path="/" component={Home} />
                    <Route path="/about" component={About} />
                </Layout>
            </Router>
        </React.Fragment>
    );
}

export default App;
