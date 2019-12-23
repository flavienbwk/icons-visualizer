import React, { Component } from 'react'
import packageJson from '../package.json';

export class About extends Component {

    render() {
        return (
            <div>
                <h2>About</h2>
                <p>Icons Visualizer is a free and open-source icons/images visualizer brought to you by <a target="_blank" rel="noopener noreferrer" href="https://flavien.berwick.fr/en">Flavien Berwick</a>.</p>
                <p>The search engine included in the Python API will try to find the images according to their filename.</p>
                <p>If you find an issue, <a target="_blank" rel="noopener noreferrer" href="https://github.com/flavienbwk/icons-visualizer/issues">please open one on Github</a>.</p>
                <hr />
                <p>Version <b>{packageJson["version"]}</b></p>
            </div>
        )
    }

    componentDidMount() {
        document.title = "About - Icons Visualizer";
    }

}
