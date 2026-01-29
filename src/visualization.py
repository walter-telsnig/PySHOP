"""
Visualization utilities for plotting SHOP results
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import pandas as pd


def setup_plot_style():
    """Configure matplotlib style for better-looking plots"""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10


def plot_reservoir_levels(reservoir_data, reservoir_names=None, save_path=None, show=True):
    """
    Plot reservoir water levels over time
    
    Args:
        reservoir_data: Dict of {reservoir_name: DataFrame/Series} or single DataFrame
        reservoir_names: List of reservoir names to plot (if reservoir_data is DataFrame)
        save_path: Path to save figure (optional)
        show: Whether to display the plot
    """
    setup_plot_style()
    fig, ax = plt.subplots()
    
    if isinstance(reservoir_data, dict):
        for name, data in reservoir_data.items():
            ax.plot(data.index, data.values, label=name, linewidth=2)
    else:
        # Assume DataFrame with multiple columns
        if reservoir_names:
            reservoir_data[reservoir_names].plot(ax=ax, linewidth=2)
        else:
            reservoir_data.plot(ax=ax, linewidth=2)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Water Level [masl]')
    ax.set_title('Reservoir Water Levels')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Format x-axis for dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_generation_and_pumping(gen_data, pump_data=None, save_path=None, show=True):
    """
    Plot generation and pumping power over time
    
    Args:
        gen_data: Generation power time series or dict
        pump_data: Pumping power time series or dict (optional)
        save_path: Path to save figure
        show: Whether to display the plot
    """
    setup_plot_style()
    fig, ax = plt.subplots()
    
    # Plot generation (positive values)
    if isinstance(gen_data, dict):
        for name, data in gen_data.items():
            ax.plot(data.index, data.values, label=f"{name} (Gen)", linewidth=2)
    else:
        ax.plot(gen_data.index, gen_data.values, label="Generation", linewidth=2, color='green')
    
    # Plot pumping (negative values for visual distinction)
    if pump_data is not None:
        if isinstance(pump_data, dict):
            for name, data in pump_data.items():
                ax.plot(data.index, -data.values, label=f"{name} (Pump)", 
                       linewidth=2, linestyle='--')
        else:
            ax.plot(pump_data.index, -pump_data.values, label="Pumping", 
                   linewidth=2, linestyle='--', color='red')
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Power [MW]')
    ax.set_title('Generation and Pumping Schedule')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_price_and_dispatch(price_data, gen_data, save_path=None, show=True):
    """
    Plot electricity price and generation dispatch on dual y-axes
    
    Args:
        price_data: Price time series
        gen_data: Generation power time series
        save_path: Path to save figure
        show: Whether to display the plot
    """
    setup_plot_style()
    fig, ax1 = plt.subplots()
    
    # Plot price on primary y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price [EUR/MWh]', color=color)
    ax1.plot(price_data.index, price_data.values, color=color, linewidth=2, alpha=0.7)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Plot generation on secondary y-axis
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Generation [MW]', color=color)
    ax2.fill_between(gen_data.index, 0, gen_data.values, color=color, alpha=0.3)
    ax2.plot(gen_data.index, gen_data.values, color=color, linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Electricity Price and Generation Dispatch')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    
    fig.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def create_summary_plot(results_dict, save_dir=None, show=True):
    """
    Create a multi-panel summary plot with all key results
    
    Args:
        results_dict: Dictionary containing:
            - 'reservoir_levels': reservoir level data
            - 'generation': generation data
            - 'pumping': pumping data (optional)
            - 'prices': price data (optional)
        save_dir: Directory to save figures
        show: Whether to display plots
    """
    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
    
    # Plot 1: Reservoir levels
    if 'reservoir_levels' in results_dict:
        save_path = save_dir / 'reservoir_levels.png' if save_dir else None
        plot_reservoir_levels(results_dict['reservoir_levels'], 
                            save_path=save_path, show=show)
    
    # Plot 2: Generation and pumping
    if 'generation' in results_dict:
        save_path = save_dir / 'dispatch.png' if save_dir else None
        plot_generation_and_pumping(
            results_dict['generation'],
            results_dict.get('pumping'),
            save_path=save_path,
            show=show
        )
    
    # Plot 3: Price and dispatch
    if 'prices' in results_dict and 'generation' in results_dict:
        save_path = save_dir / 'price_dispatch.png' if save_dir else None
        plot_price_and_dispatch(
            results_dict['prices'],
            results_dict['generation'],
            save_path=save_path,
            show=show
        )
