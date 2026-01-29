"""
SHOP session management utilities
"""

import os
from pathlib import Path
from pyshop import ShopSession


class ShopManager:
    """Wrapper around ShopSession with project-specific configuration"""
    
    def __init__(self, license_path=None, solver_path=None, silent=False, log_file=None):
        """
        Initialize SHOP session with project defaults
        
        Args:
            license_path: Path to SHOP license file (defaults to ./Licence directory)
            solver_path: Path to SHOP solver binaries (defaults to ./Licence directory)
            silent: Suppress console output
            log_file: Path to log file for debugging
        """
        # Set default paths to Licence folder if not provided
        project_root = Path(__file__).parent.parent
        licence_dir = project_root / "Licence"
        
        if license_path is None:
            license_path = licence_dir
        if solver_path is None:
            solver_path = licence_dir
            
        self.license_path = str(license_path) if license_path else None
        self.solver_path = str(solver_path) if solver_path else None
        
        # Create SHOP session
        self.shop = ShopSession(
            license_path=self.license_path,
            solver_path=self.solver_path,
            silent=silent,
            log_file=log_file if log_file else ""
        )
        
    def set_time(self, starttime, endtime, timeresolution=1, timeunit='hour'):
        """
        Set optimization time period
        
        Args:
            starttime: Start time as string "YYYY-MM-DD HH:MM:SS", datetime, or Timestamp
            endtime: End time as string "YYYY-MM-DD HH:MM:SS", datetime, or Timestamp
            timeresolution: Time resolution (default: 1 hour)
            timeunit: Unit for resolution ('hour' or 'minute', default: 'hour')
        """
        import pandas as pd
        from datetime import datetime
        
        # Convert to pandas Timestamps
        if isinstance(starttime, str):
            starttime = pd.Timestamp(starttime)
        if isinstance(endtime, str):
            endtime = pd.Timestamp(endtime)
        if isinstance(starttime, datetime):
            starttime = pd.Timestamp(starttime)
        if isinstance(endtime, datetime):
            endtime = pd.Timestamp(endtime)
            
        # robust format using pd.Series for timeresolution (as used in SINTEF examples)
        res_series = pd.Series(index=[starttime], data=[timeresolution])
        
        self.shop.set_time_resolution(
            starttime=starttime,
            endtime=endtime,
            timeunit=timeunit,
            timeresolution=res_series
        )
        
    def get_model(self):
        """Get the SHOP model object for building topology"""
        return self.shop.model
    
    def run_optimization(self, full_iterations=5, incremental_iterations=3):
        """
        Run SHOP optimization with full and incremental phases
        """
        # Set code flag to full and run initial iterations
        self.shop.set_code(['full'], [])
        self.shop.start_sim([], [str(full_iterations)])
        
        # Set code flag to incremental and run final iterations
        self.shop.set_code(['incremental'], [])
        self.shop.start_sim([], [str(incremental_iterations)])
        
    def save_results(self, output_dir):
        """
        Save optimization results to directory
        
        Args:
            output_dir: Directory path to save results
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save results in different formats
        # This can be extended based on SHOP's save functionality
        pass
    
    def plot_topology(self, filename="topology", show=True):
        """
        Generate topology visualization
        
        Args:
            filename: Output filename (without extension)
            show: Whether to display the plot
        """
        self.shop.model.build_connection_tree(filename=filename, write_file=True)
