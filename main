import React, { useState, useEffect } from 'react';
import { AlertTriangle, Camera, MapPin, Clock, Users, Car, Zap, CheckCircle, XCircle, Play, Pause, RotateCcw, Phone, Navigation, X } from 'lucide-react';

const TrafficDashboard = () => {
  const [selectedJunction, setSelectedJunction] = useState('anna-salai-mount');
  const [emergencyMode, setEmergencyMode] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [manualOverride, setManualOverride] = useState(false);
  const [selectedIncident, setSelectedIncident] = useState(null);
  
  // Simulated real-time data
  const [dashboardData, setDashboardData] = useState({
    junctions: {
      'anna-salai-mount': {
        name: 'Anna Salai - Mount Road',
        density: 85,
        queueLength: 12,
        waitTime: 95,
        status: 'high',
        phase: 'NS Green',
        timeLeft: 28,
        emergencyVehicle: false,
        accident: false,
        lat: 13.0827,
        lng: 80.2707,
        cycleLength: 120,
        phases: ['NS Green', 'NS Yellow', 'NS Red', 'EW Green', 'EW Yellow', 'EW Red']
      },
      'omr-sholinganallur': {
        name: 'OMR - Sholinganallur',
        density: 62,
        queueLength: 8,
        waitTime: 45,
        status: 'medium',
        phase: 'EW Green',
        timeLeft: 15,
        emergencyVehicle: true,
        accident: false,
        lat: 12.9010,
        lng: 80.2279,
        cycleLength: 90,
        phases: ['NS Green', 'NS Yellow', 'NS Red', 'EW Green', 'EW Yellow', 'EW Red']
      },
      'ecr-mahabalipuram': {
        name: 'ECR - Mahabalipuram Rd',
        density: 34,
        queueLength: 4,
        waitTime: 22,
        status: 'low',
        phase: 'NS Red',
        timeLeft: 8,
        emergencyVehicle: false,
        accident: true,
        lat: 12.8340,
        lng: 80.2880,
        cycleLength: 100,
        phases: ['NS Green', 'NS Yellow', 'NS Red', 'EW Green', 'EW Yellow', 'EW Red']
      }
    },
    incidents: [
      {
        id: 1,
        type: 'emergency',
        location: 'OMR Junction',
        message: 'Ambulance approaching from south',
        time: '14:23',
        priority: 'high',
        image: '/api/placeholder/200/150',
        details: 'Emergency vehicle detected via OpenCV. Estimated arrival: 2 minutes.',
        actions: ['Clear traffic signal', 'Alert nearby junctions', 'Contact emergency services'],
        resolved: false,
        vehicleType: 'Ambulance',
        direction: 'South to North',
        estimatedArrival: '2 min'
      },
      {
        id: 2,
        type: 'accident',
        location: 'ECR Junction',
        message: 'Minor collision detected',
        time: '14:20',
        priority: 'medium',
        image: '/api/placeholder/200/150',
        details: 'OpenCV detected sudden stop pattern. 2 vehicles involved, minor damage.',
        actions: ['Dispatch traffic police', 'Contact nearest hospital', 'Redirect traffic', 'Clear debris'],
        resolved: false,
        severity: 'Minor',
        vehiclesInvolved: 2,
        injuries: 'None reported'
      },
      {
        id: 3,
        type: 'congestion',
        location: 'Anna Salai',
        message: 'Queue length exceeding threshold',
        time: '14:18',
        priority: 'low',
        image: '/api/placeholder/200/150',
        details: 'Vehicle queue detected at 15+ vehicles. Suggested timing adjustment.',
        actions: ['Extend green phase', 'Optimize signal timing', 'Monitor queue length'],
        resolved: false,
        queueLength: 15,
        suggestion: 'Extend NS green by 20s'
      }
    ]
  });

  const [aiRecommendation, setAiRecommendation] = useState({
    suggestion: 'Extend NS green phase by 15s to clear queue',
    confidence: 93,
    reason: 'High density detected, queue length increasing',
    accepted: null
  });

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Signal phase management
  useEffect(() => {
    if (!manualOverride) {
      const interval = setInterval(() => {
        setDashboardData(prev => {
          const newJunctions = { ...prev.junctions };
          
          Object.keys(newJunctions).forEach(key => {
            const junction = newJunctions[key];
            if (junction.timeLeft > 0) {
              junction.timeLeft -= 1;
            } else {
              // Move to next phase
              const currentPhaseIndex = junction.phases.indexOf(junction.phase);
              const nextPhaseIndex = (currentPhaseIndex + 1) % junction.phases.length;
              junction.phase = junction.phases[nextPhaseIndex];
              
              // Set time for new phase
              if (junction.phase.includes('Yellow')) {
                junction.timeLeft = 5;
              } else if (junction.phase.includes('Green')) {
                junction.timeLeft = emergencyMode ? 60 : 30;
              } else {
                junction.timeLeft = emergencyMode ? 20 : 25;
              }
            }
          });
          
          return { ...prev, junctions: newJunctions };
        });
      }, 1000);
      
      return () => clearInterval(interval);
    }
  }, [manualOverride, emergencyMode]);

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setDashboardData(prev => ({
        ...prev,
        junctions: {
          ...prev.junctions,
          [selectedJunction]: {
            ...prev.junctions[selectedJunction],
            density: Math.max(10, Math.min(100, prev.junctions[selectedJunction].density + (Math.random() - 0.5) * 5)),
            waitTime: Math.max(5, prev.junctions[selectedJunction].waitTime + (Math.random() - 0.5) * 10)
          }
        }
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, [selectedJunction]);

  const handleAcceptRecommendation = () => {
    setAiRecommendation(prev => ({ ...prev, accepted: true }));
    // Apply the recommendation
    setDashboardData(prev => ({
      ...prev,
      junctions: {
        ...prev.junctions,
        [selectedJunction]: {
          ...prev.junctions[selectedJunction],
          timeLeft: prev.junctions[selectedJunction].timeLeft + 15
        }
      }
    }));
    
    // Generate new recommendation after 5 seconds
    setTimeout(() => {
      setAiRecommendation({
        suggestion: 'Optimize EW phase timing based on queue analysis',
        confidence: 87,
        reason: 'Traffic pattern analysis suggests timing adjustment',
        accepted: null
      });
    }, 5000);
  };

  const handleDeclineRecommendation = () => {
    setAiRecommendation(prev => ({ ...prev, accepted: false }));
    
    // Generate new recommendation after 3 seconds
    setTimeout(() => {
      setAiRecommendation({
        suggestion: 'Consider emergency vehicle priority routing',
        confidence: 91,
        reason: 'Emergency vehicle detected in nearby junction',
        accepted: null
      });
    }, 3000);
  };

  const handleManualSignalControl = (phase) => {
    if (manualOverride) {
      setDashboardData(prev => ({
        ...prev,
        junctions: {
          ...prev.junctions,
          [selectedJunction]: {
            ...prev.junctions[selectedJunction],
            phase: phase,
            timeLeft: 30
          }
        }
      }));
    }
  };

  const handleEmergencyPreemption = () => {
    setEmergencyMode(true);
    setDashboardData(prev => ({
      ...prev,
      junctions: {
        ...prev.junctions,
        [selectedJunction]: {
          ...prev.junctions[selectedJunction],
          phase: 'NS Green',
          timeLeft: 60
        }
      }
    }));
  };

  const handleResolveIncident = (incidentId, action) => {
    setDashboardData(prev => ({
      ...prev,
      incidents: prev.incidents.map(incident =>
        incident.id === incidentId
          ? { ...incident, resolved: true, resolvedAction: action, resolvedTime: new Date().toLocaleTimeString() }
          : incident
      )
    }));

    // Simulate action execution
    if (action === 'Contact nearest hospital') {
      alert('📞 Contacted Apollo Hospital Chennai - ETA: 8 minutes');
    } else if (action === 'Dispatch traffic police') {
      alert('🚔 Traffic police dispatched from T. Nagar station - ETA: 5 minutes');
    } else if (action === 'Clear traffic signal') {
      handleEmergencyPreemption();
      alert('🚦 Emergency signal preemption activated');
    } else if (action === 'Alert nearby junctions') {
      alert('⚠️ Nearby junctions alerted - Emergency corridor established');
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'high': return 'text-red-500 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-500 bg-gray-100';
    }
  };

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return 'border-l-red-500 bg-red-50';
      case 'medium': return 'border-l-yellow-500 bg-yellow-50';
      case 'low': return 'border-l-blue-500 bg-blue-50';
      default: return 'border-l-gray-500 bg-gray-50';
    }
  };

  const getPhaseColor = (phase) => {
    if (phase.includes('Green')) return 'text-green-400';
    if (phase.includes('Yellow')) return 'text-yellow-400';
    if (phase.includes('Red')) return 'text-red-400';
    return 'text-gray-400';
  };

  const currentJunction = dashboardData.junctions[selectedJunction];

  return (
    <div className="h-screen bg-gray-900 text-white flex flex-col">
      {/* Header */}
      <div className="bg-gray-800 p-4 flex justify-between items-center border-b border-gray-700">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold text-blue-400">Chennai Traffic Control</h1>
          <div className="text-sm text-gray-300">
            {currentTime.toLocaleTimeString()}
          </div>
        </div>
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm">System Online</span>
          </div>
          <div className="text-sm">
            Active Incidents: <span className="text-red-400 font-bold">{dashboardData.incidents.filter(i => !i.resolved).length}</span>
          </div>
          <button 
            onClick={() => setEmergencyMode(!emergencyMode)}
            className={`px-4 py-2 rounded font-medium transition-colors ${emergencyMode ? 'bg-red-600 text-white' : 'bg-gray-600 text-gray-300 hover:bg-gray-500'}`}
          >
            {emergencyMode ? 'Emergency Mode ON' : 'Emergency Mode OFF'}
          </button>
        </div>
      </div>

      <div className="flex-1 flex">
        {/* Left Panel - Metrics & Incidents */}
        <div className="w-1/4 bg-gray-800 p-4 space-y-4 overflow-y-auto">
          {/* Junction Selector */}
          <div>
            <h3 className="text-sm font-semibold mb-2 text-gray-300">Selected Junction</h3>
            <select 
              value={selectedJunction}
              onChange={(e) => setSelectedJunction(e.target.value)}
              className="w-full bg-gray-700 text-white p-2 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
            >
              {Object.entries(dashboardData.junctions).map(([key, junction]) => (
                <option key={key} value={key}>{junction.name}</option>
              ))}
            </select>
          </div>

          {/* Live Metrics */}
          <div className="bg-gray-700 p-3 rounded">
            <h3 className="text-sm font-semibold mb-3 text-gray-300">Live Metrics</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Traffic Density</span>
                <div className="flex items-center space-x-2">
                  <div className="w-20 bg-gray-600 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full transition-all duration-500 ${currentJunction.density > 70 ? 'bg-red-500' : currentJunction.density > 40 ? 'bg-yellow-500' : 'bg-green-500'}`}
                      style={{width: `${currentJunction.density}%`}}
                    ></div>
                  </div>
                  <span className="text-sm font-bold">{Math.round(currentJunction.density)}%</span>
                </div>
              </div>
              
              <div className="flex justify-between">
                <span className="text-xs text-gray-400">Queue Length</span>
                <span className="text-sm font-bold">{currentJunction.queueLength} vehicles</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-xs text-gray-400">Avg Wait Time</span>
                <span className="text-sm font-bold">{Math.round(currentJunction.waitTime)}s</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-xs text-gray-400">Current Phase</span>
                <span className={`text-sm font-bold ${getPhaseColor(currentJunction.phase)}`}>
                  {currentJunction.phase}
                </span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-xs text-gray-400">Time Left</span>
                <span className="text-sm font-bold">{currentJunction.timeLeft}s</span>
              </div>
              
              {manualOverride && (
                <div className="bg-yellow-900 p-2 rounded border border-yellow-600">
                  <span className="text-xs text-yellow-300 font-medium">Manual Override Active</span>
                </div>
              )}
            </div>
          </div>

          {/* Incident Feed */}
          <div className="bg-gray-700 p-3 rounded flex-1">
            <h3 className="text-sm font-semibold mb-3 text-gray-300">Live Incidents</h3>
            <div className="space-y-2">
              {dashboardData.incidents.filter(i => !i.resolved).map(incident => (
                <div key={incident.id} className={`border-l-4 pl-3 py-2 rounded cursor-pointer hover:bg-opacity-80 ${getPriorityColor(incident.priority)}`}>
                  <div className="flex items-center space-x-2 mb-1">
                    {incident.type === 'emergency' && <Zap className="w-4 h-4 text-red-500" />}
                    {incident.type === 'accident' && <AlertTriangle className="w-4 h-4 text-yellow-500" />}
                    {incident.type === 'congestion' && <Users className="w-4 h-4 text-blue-500" />}
                    <span className="text-xs font-medium text-gray-800">{incident.location}</span>
                    <span className="text-xs text-gray-600">{incident.time}</span>
                  </div>
                  <p className="text-xs text-gray-700 mb-2">{incident.message}</p>
                  <div className="flex space-x-2">
                    <button 
                      onClick={() => setSelectedIncident(incident)}
                      className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-2 py-1 rounded transition-colors"
                    >
                      View
                    </button>
                    <button 
                      onClick={() => handleResolveIncident(incident.id, incident.actions[0])}
                      className="text-xs bg-green-600 hover:bg-green-700 text-white px-2 py-1 rounded transition-colors"
                    >
                      Resolve
                    </button>
                  </div>
                </div>
              ))}
              
              {dashboardData.incidents.filter(i => i.resolved).length > 0 && (
                <div className="mt-4 pt-2 border-t border-gray-600">
                  <h4 className="text-xs font-semibold text-gray-400 mb-2">Recently Resolved</h4>
                  {dashboardData.incidents.filter(i => i.resolved).slice(-2).map(incident => (
                    <div key={incident.id} className="bg-green-900 bg-opacity-50 p-2 rounded mb-2">
                      <div className="flex items-center space-x-1">
                        <CheckCircle className="w-3 h-3 text-green-400" />
                        <span className="text-xs text-green-300">{incident.location}</span>
                      </div>
                      <p className="text-xs text-green-200">Resolved: {incident.resolvedAction}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Center - Map View */}
        <div className="flex-1 bg-gray-700 relative">
          <div className="absolute top-4 left-4 bg-gray-800 p-2 rounded z-10">
            <h3 className="text-sm font-semibold text-gray-300 mb-2">Chennai Traffic Map</h3>
            <p className="text-xs text-gray-400">Real-time junction monitoring</p>
          </div>
          
          {/* OpenStreetMap Integration Placeholder */}
          <div className="w-full h-full relative bg-gradient-to-br from-slate-600 via-slate-700 to-slate-800">
            {/* Map background with street-like pattern */}
            <div className="absolute inset-0 opacity-30">
              <svg width="100%" height="100%" className="text-gray-600">
                <defs>
                  <pattern id="street-grid" x="0" y="0" width="50" height="50" patternUnits="userSpaceOnUse">
                    <path d="M 50 0 L 0 0 0 50" fill="none" stroke="currentColor" strokeWidth="1"/>
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#street-grid)" />
              </svg>
            </div>
            
            {/* Junction Points with realistic Chennai locations */}
            {Object.entries(dashboardData.junctions).map(([key, junction], index) => (
              <div
                key={key}
                className={`absolute transform -translate-x-3 -translate-y-3 cursor-pointer transition-all duration-300 ${
                  selectedJunction === key ? 'scale-150 z-20' : 'hover:scale-125 z-10'
                }`}
                style={{
                  top: `${25 + index * 20}%`,
                  left: `${15 + index * 35}%`
                }}
                onClick={() => setSelectedJunction(key)}
              >
                <div className={`w-8 h-8 rounded-full border-2 border-white shadow-lg ${
                  selectedJunction === key ? 'ring-4 ring-blue-400 ring-opacity-60' : ''
                } ${
                  junction.emergencyVehicle ? 'bg-red-500 animate-pulse' : 
                  junction.accident ? 'bg-yellow-500' :
                  junction.density > 70 ? 'bg-red-400' :
                  junction.density > 40 ? 'bg-yellow-400' : 'bg-green-400'
                }`}>
                  {/* Signal indicator */}
                  <div className={`absolute -top-1 -right-1 w-3 h-3 rounded-full ${getPhaseColor(junction.phase).replace('text-', 'bg-')}`}></div>
                </div>
                
                <div className={`absolute -bottom-12 -left-12 text-xs whitespace-nowrap bg-gray-800 px-2 py-1 rounded shadow-lg transition-opacity ${
                  selectedJunction === key ? 'opacity-100' : 'opacity-0 hover:opacity-100'
                }`}>
                  <div className="text-white font-medium">{junction.name.split(' - ')[0]}</div>
                  <div className={`text-xs ${getPhaseColor(junction.phase)}`}>
                    {junction.phase} • {junction.timeLeft}s
                  </div>
                  <div className="text-xs text-gray-300">
                    Density: {Math.round(junction.density)}%
                  </div>
                </div>
              </div>
            ))}
            
            {/* Traffic flow indicators */}
            <div className="absolute bottom-20 left-4 space-y-1">
              {[...Array(3)].map((_, i) => (
                <div key={i} className={`w-2 h-8 rounded-full animate-pulse ${
                  i === 0 ? 'bg-green-400' : i === 1 ? 'bg-yellow-400' : 'bg-red-400'
                }`} style={{ animationDelay: `${i * 0.5}s` }}></div>
              ))}
            </div>
            
            {/* Density Heatmap Legend */}
            <div className="absolute bottom-4 left-4 bg-gray-800 bg-opacity-90 p-3 rounded shadow-lg">
              <h4 className="text-xs font-semibold mb-2 text-white">Traffic Density</h4>
              <div className="space-y-1 text-xs">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                  <span className="text-gray-300">Low (0-40%)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <span className="text-gray-300">Medium (40-70%)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                  <span className="text-gray-300">High (70%+)</span>
                </div>
                <div className="flex items-center space-x-2 mt-2 pt-1 border-t border-gray-600">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                  <span className="text-gray-300">Emergency</span>
                </div>
              </div>
            </div>

            {/* Map attribution (OpenStreetMap) */}
            <div className="absolute bottom-4 right-4 text-xs text-gray-400 bg-gray-800 bg-opacity-80 px-2 py-1 rounded">
              © OpenStreetMap contributors
            </div>
          </div>
        </div>

        {/* Right Panel - AI Recommendations & Controls */}
        <div className="w-1/4 bg-gray-800 p-4 space-y-4 overflow-y-auto">
          {/* AI Decision Support */}
          <div className="bg-gray-700 p-3 rounded">
            <h3 className="text-sm font-semibold mb-3 text-gray-300">AI Recommendations</h3>
            <div className="space-y-3">
              {aiRecommendation.accepted === null && (
                <div className="bg-blue-900 p-3 rounded border border-blue-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-medium text-blue-300">RL Model Suggestion</span>
                    <span className="text-xs text-blue-400">{aiRecommendation.confidence}% confidence</span>
                  </div>
                  <p className="text-xs text-blue-200 mb-2">{aiRecommendation.suggestion}</p>
                  <p className="text-xs text-blue-300 opacity-80 mb-3">{aiRecommendation.reason}</p>
                  <div className="flex space-x-2">
                    <button 
                      onClick={handleAcceptRecommendation}
                      className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded transition-colors"
                    >
                      Accept
                    </button>
                    <button 
                      onClick={handleDeclineRecommendation}
                      className="text-xs bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded transition-colors"
                    >
                      Decline
                    </button>
                  </div>
                </div>
              )}
              
              {aiRecommendation.accepted === true && (
                <div className="bg-green-900 p-3 rounded border border-green-700">
                  <div className="flex items-center space-x-2 mb-1">
                    <CheckCircle className="w-4 h-4 text-green-400" />
                    <span className="text-xs font-medium text-green-300">Recommendation Applied</span>
                  </div>
                  <p className="text-xs text-green-200">Signal timing adjusted successfully</p>
                </div>
              )}
              
              {aiRecommendation.accepted === false && (
                <div className="bg-red-900 p-3 rounded border border-red-700">
                  <div className="flex items-center space-x-2 mb-1">
                    <XCircle className="w-4 h-4 text-red-400" />
                    <span className="text-xs font-medium text-red-300">Recommendation Declined</span>
                  </div>
                  <p className="text-xs text-red-200">Manual control maintained</p>
                </div>
              )}
              
              <div className="bg-green-900 p-2 rounded border border-green-700">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-medium text-green-300">OpenCV Detection</span>
                  <span className="text-xs text-green-400">Active</span>
                </div>
                <p className="text-xs text-green-200">Traffic flow analysis running</p>
              </div>
            </div>
          </div>

          {/* Signal Controls */}
          <div className="bg-gray-700 p-3 rounded">
            <h3 className="text-sm font-semibold mb-3 text-gray-300">Signal Control</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Manual Override</span>
                <button 
                  onClick={() => setManualOverride(!manualOverride)}
                  className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                    manualOverride ? 'bg-red-600 hover:bg-red-700 text-white' : 'bg-gray-600 hover:bg-gray-500 text-white'
                  }`}
                >
                  {manualOverride ? 'Override ON' : 'Override OFF'}
                </button>
              </div>
              
              <div className="grid grid-cols-2 gap-2 mt-3">
                <button 
                  onClick={() => handleManualSignalControl('NS Green')}
                  disabled={!manualOverride}
                  className={`p-2 rounded text-xs font-medium transition-colors ${
                    !manualOverride 
                      ? 'bg-gray-600 text-gray-400 cursor-not-allowed' 
                      : currentJunction.phase === 'NS Green'
                        ? 'bg-green-600 text-white'
                        : 'bg-green-500 hover:bg-green-600 text-white'
                  }`}
                >
                  NS Green
                </button>
                <button 
                  onClick={() => handleManualSignalControl('NS Red')}
                  disabled={!manualOverride}
                  className={`p-2 rounded text-xs font-medium transition-colors ${
                    !manualOverride 
                      ? 'bg-gray-600 text-gray-400 cursor-not-allowed' 
                      : currentJunction.phase === 'NS Red'
                        ? 'bg-red-600 text-white'
                        : 'bg-red-500 hover:bg-red-600 text-white'
                  }`}
                >
                  NS Red
                </button>
                <button 
                  onClick={() => handleManualSignalControl('EW Green')}
                  disabled={!manualOverride}
                  className={`p-2 rounded text-xs font-medium transition-colors ${
                    !manualOverride 
                      ? 'bg-gray-600 text-gray-400 cursor-not-allowed' 
                      : currentJunction.phase === 'EW Green'
                        ? 'bg-green-600 text-white'
                        : 'bg-green-500 hover:bg-green-600 text-white'
                  }`}
                >
                  EW Green
                </button>
                <button 
                  onClick={() => handleManualSignalControl('EW Red')}
                  disabled={!manualOverride}
                  className={`p-2 rounded text-xs font-medium transition-colors ${
                    !manualOverride 
                      ? 'bg-gray-600 text-gray-400 cursor-not-allowed' 
                      : currentJunction.phase === 'EW Red'
                        ? 'bg-red-600 text-white'
                        : 'bg-red-500 hover:bg-red-600 text-white'
                  }`}
                >
                  EW Red
                </button>
              </div>
              
              <div className="mt-3">
                <button 
                  onClick={handleEmergencyPreemption}
                  className="w-full bg-yellow-600 hover:bg-yellow-700 text-white p-2 rounded text-xs font-medium transition-colors"
                >
                  Emergency Preemption
                </button>
              </div>
            </div>
          </div>

          {/* System Health */}
          <div className="bg-gray-700 p-3 rounded">
            <h3 className="text-sm font-semibold mb-3 text-gray-300">System Health</h3>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Cameras Online</span>
                <div className="flex items-center space-x-1">
                  <CheckCircle className="w-3 h-3 text-green-400" />
                  <span className="text-xs text-green-400">24/24</span>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Model Performance</span>
                <div className="flex items-center space-x-1">
                  <CheckCircle className="w-3 h-3 text-green-400" />
                  <span className="text-xs text-green-400">98.5%</span>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Network Latency</span>
                <div className="flex items-center space-x-1">
                  <CheckCircle className="w-3 h-3 text-green-400" />
                  <span className="text-xs text-green-400">12ms</span>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Data Processing</span>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-xs text-green-400">Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Incident Detail Modal */}
      {selectedIncident && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-6 rounded-lg max-w-2xl w-full mx-4 max-h-screen overflow-y-auto">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-lg font-bold text-white mb-1">
                  {selectedIncident.type === 'emergency' && '🚨 Emergency Vehicle'}
                  {selectedIncident.type === 'accident' && '⚠️ Traffic Accident'}
                  {selectedIncident.type === 'congestion' && '🚗 Traffic Congestion'}
                </h2>
                <p className="text-sm text-gray-300">{selectedIncident.location} • {selectedIncident.time}</p>
              </div>
              <button 
                onClick={() => setSelectedIncident(null)}
                className="text-gray-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <img 
                  src={selectedIncident.image} 
                  alt="Incident view"
                  className="w-full h-40 object-cover rounded bg-gray-700"
                />
                <p className="text-xs text-gray-400 mt-1">Live camera feed</p>
              </div>
              
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-semibold text-gray-300 mb-1">Details</h4>
                  <p className="text-sm text-gray-200">{selectedIncident.details}</p>
                </div>
                
                {selectedIncident.type === 'emergency' && (
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-400">Vehicle Type:</span>
                      <span className="text-xs text-white">{selectedIncident.vehicleType}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-400">Direction:</span>
                      <span className="text-xs text-white">{selectedIncident.direction}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-400">ETA:</span>
                      <span className="text-xs text-red-400">{selectedIncident.estimatedArrival}</span>
                    </div>
                  </div>
                )}
                
                {selectedIncident.type === 'accident' && (
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-400">Severity:</span>
                      <span className="text-xs text-yellow-400">{selectedIncident.severity}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-400">Vehicles:</span>
                      <span className="text-xs text-white">{selectedIncident.vehiclesInvolved}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-400">Injuries:</span>
                      <span className="text-xs text-green-400">{selectedIncident.injuries}</span>
                    </div>
                  </div>
                )}
                
                {selectedIncident.type === 'congestion' && (
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-400">Queue Length:</span>
                      <span className="text-xs text-white">{selectedIncident.queueLength} vehicles</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-xs text-gray-400">AI Suggestion:</span>
                      <span className="text-xs text-blue-400">{selectedIncident.suggestion}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-gray-300 mb-3">Available Actions</h4>
              <div className="grid grid-cols-2 gap-2">
                {selectedIncident.actions.map((action, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      handleResolveIncident(selectedIncident.id, action);
                      setSelectedIncident(null);
                    }}
                    className={`p-3 rounded text-sm font-medium transition-colors ${
                      action.includes('emergency') || action.includes('hospital') 
                        ? 'bg-red-600 hover:bg-red-700 text-white' 
                        : action.includes('police') 
                        ? 'bg-blue-600 hover:bg-blue-700 text-white'
                        : action.includes('Clear') || action.includes('Alert')
                        ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
                        : 'bg-green-600 hover:bg-green-700 text-white'
                    }`}
                  >
                    {action.includes('hospital') && <Phone className="w-4 h-4 inline mr-1" />}
                    {action.includes('police') && <Navigation className="w-4 h-4 inline mr-1" />}
                    {action}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TrafficDashboard;
