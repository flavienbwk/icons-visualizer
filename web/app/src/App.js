import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './Home';
import { About } from './About';
import { Layout } from './Layout';
import { NavigationBar } from './NavigationBar';

function App() {

    return (
        <React.Fragment>
            <Router basename={"/"}>
                <NavigationBar />
                <Layout>
                    <Switch>
                        <Route exact path="/" component={Home} />
                        <Route path="/about" component={About} />
                    </Switch>
                </Layout>
            </Router>
        </React.Fragment>
    );
}

export default App;
