import { useEffect } from 'react';

export function BarChart() {
  useEffect(() => {
    var divElement = document.getElementById('viz1633158910517');
    var vizElement = divElement.getElementsByTagName('object')[0];
    vizElement.style.width = '100%';
    vizElement.style.height = divElement.offsetWidth * 0.75 + 'px';
    var scriptElement = document.createElement('script');
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    vizElement.parentNode.insertBefore(scriptElement, vizElement);
  }, []);

  return (
    <div>
      <div className="tableauPlaceholder" id="viz1633158910517" style={{ position: 'relative' }}>
        <noscript>
          <a href="#">
            <img
              alt="Total Yearly Potential Solar Energy Generation "
              src="https://public.tableau.com/static/images/Ha/HackOnCloud/SolarEnergyGenerationPotential-MyLocation2/1_rss.png"
              style={{ border: 'none' }}
            />
          </a>
        </noscript>
        <object className="tableauViz" style={{ display: 'none' }}>
          <param name="host_url" value="https%3A%2F%2Fpublic.tableau.com%2F" />{' '}
          <param name="embed_code_version" value="3" /> <param name="site_root" value="" />{' '}
          <param name="name" value="HackOnCloud/SolarEnergyGenerationPotential-MyLocation2" />
          <param name="tabs" value="no" />
          <param name="toolbar" value="yes" />{' '}
          <param
            name="static_image"
            value="https://public.tableau.com/static/images/Ha/HackOnCloud/SolarEnergyGenerationPotential-MyLocation2/1.png"
          />
          <param name="animate_transition" value="yes" /> <param name="display_static_image" value="yes" />
          <param name="display_spinner" value="yes" />
          <param name="display_overlay" value="yes" />
          <param name="display_count" value="yes" />
          <param name="language" value="en-US" />
          <param name="filter" value="publish=yes" />
        </object>
      </div>
    </div>
  );
}