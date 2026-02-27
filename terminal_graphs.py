"""
Terminal-based graphing package for real-time data visualization.
Provides bar graphs and smooth sine wave displays using ASCII characters.
"""

class ShoeAnimation:
    """
    Handles ASCII shoe animation that progresses through walking states based on sine wave position.
    """
    def __init__(self):
        self.shoe_states = {
            'ready': "👟 Step: [▬▬▬] Ready",
            'lifting': "👟 Step: [▬▬▬] Lifting...",
            'striding': "👟 Step: [▬▬▬] ↗ Striding",
            'landing': "👟 Step: [▬▬▬] ↘ Landing!"
        }
        self.landing_message = "🦶 STEP LANDED! 🦶"
    
    def get_shoe_state(self, sine_value, step_detected):
        """
        Determine the appropriate shoe state based on sine wave position and step detection.
        
        Args:
            sine_value: Current sine wave value (-1 to 1)
            step_detected: Boolean indicating if a step peak was detected
            
        Returns:
            String with the appropriate shoe animation for current walking phase
        """
        if step_detected and sine_value >= 0.5:
            # Landing state - triggered at sine wave peaks (step detection)
            return self.shoe_states['landing']
        elif sine_value >= 0.3:
            # Striding state - foot in air, approaching peak
            return self.shoe_states['striding']
        elif sine_value >= -0.3:
            # Lifting state - foot lifting off ground
            return self.shoe_states['lifting']
        else:
            # Ready state - foot flat on ground, between steps
            return self.shoe_states['ready']
    
    def get_landing_line(self, step_detected):
        """
        Get the landing line that only shows when a step is detected.
        
        Args:
            step_detected: Boolean indicating if a step peak was detected
            
        Returns:
            String with landing message if step detected, empty string otherwise
        """
        return self.landing_message if step_detected else ""

class DataBuffer:
    """
    Circular buffer to store recent data points for visualization.
    """
    def __init__(self, size=60):
        self.size = size
        self.buffer = [0.0] * size
        self.index = 0
        self.has_data = False
    
    def add_value(self, value):
        """Add a new value to the buffer."""
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size
        self.has_data = True
    
    def get_display_values(self):
        """Get values in display order (oldest to newest)."""
        return self.buffer[self.index:] + self.buffer[:self.index]
    
    def get_current_value(self):
        """Get the most recently added value."""
        if not self.has_data:
            return None
        # The current value is at the previous index (since we increment after storing)
        current_index = (self.index - 1) % self.size
        return self.buffer[current_index]


class BarGraph:
    """
    Horizontal bar graph for displaying single values.
    """
    def __init__(self, width=50, value_range=(0, 10), label="Value"):
        self.width = width
        self.min_val, self.max_val = value_range
        self.label = label
    
    def plot(self, value):
        """Plot a single value as a horizontal bar."""
        # Clamp value to range
        clamped_value = max(self.min_val, min(value, self.max_val))
        
        # Normalize to 0-1 range
        normalized = (clamped_value - self.min_val) / (self.max_val - self.min_val)
        
        # Create bar
        bar_length = int(normalized * self.width)
        bar = '#' * bar_length
        
        print(f"{self.label}: {value:5.2f} | {bar}")


class SineWaveGraph:
    """
    Animated sine wave visualization showing temporal progression with trail effect.
    """
    def __init__(self, width=60, height=9, value_range=(-1, 1)):
        self.width = width
        self.height = height
        self.min_val, self.max_val = value_range
        self.buffer = DataBuffer(width)
        
        # Create row labels
        self.row_labels = []
        for i in range(height):
            # Map row index to value (top row = max_val, bottom row = min_val)
            row_value = self.max_val - (i * (self.max_val - self.min_val) / (height - 1))
            if abs(row_value) < 0.01:  # Handle near-zero values
                self.row_labels.append(" 0.0 |")
            else:
                self.row_labels.append(f"{row_value:5.2f}|")
    
    def _value_to_row(self, value):
        """Convert a value to its corresponding row position (0 = top, height-1 = bottom)."""
        # Clamp value to range
        clamped = max(self.min_val, min(value, self.max_val))
        
        # Normalize to 0-1 range, then scale to row range
        normalized = (clamped - self.min_val) / (self.max_val - self.min_val)
        row = (1 - normalized) * (self.height - 1)  # Invert because row 0 is top
        
        return row
    

class DualGraph:
    """
    Combines bar graph and sine wave for dual visualization with in-place updates.
    """
    def __init__(self, bar_width=50, bar_range=(7.8, 11.8), 
                 sine_width=60, sine_height=9, sine_range=(-1, 1)):
        self.bar_graph = BarGraph(bar_width, bar_range, "Accel")
        self.sine_graph = SineWaveGraph(sine_width, sine_height, sine_range)
        self.shoe_animation = ShoeAnimation()
        self.first_render = True
        self.total_lines = 4 + sine_height  # 1 bar + 1 shoe animation + 1 landing line + 1 spacing + sine_height lines
    
    def plot(self, accel_value, sine_value, step_impact=False):
        """Plot both the accelerometer bar and sine wave point with in-place updates."""
        # Add sine wave data point
        self.sine_graph.buffer.add_value(sine_value)
        
        # If not first render, move cursor up to overwrite previous output
        if not self.first_render:
            print(f"\033[{self.total_lines}A", end="")
        
        # Render bar graph
        print("\033[2K", end="")  # Clear line
        clamped_value = max(self.bar_graph.min_val, min(accel_value, self.bar_graph.max_val))
        normalized = (clamped_value - self.bar_graph.min_val) / (self.bar_graph.max_val - self.bar_graph.min_val)
        bar_length = int(normalized * self.bar_graph.width)
        bar = '#' * bar_length
        print(f"Accel: {accel_value:5.2f} | {bar}")
        
        # Render shoe animation (after bar, before wave)
        print("\033[2K", end="")  # Clear line
        shoe_state = self.shoe_animation.get_shoe_state(sine_value, step_impact)
        print(shoe_state)
        
        # Render landing line (only shows when step lands)
        print("\033[2K", end="")  # Clear line
        landing_line = self.shoe_animation.get_landing_line(step_impact)
        print(landing_line)
        
        # Spacing line
        print("\033[2K")  # Clear line and move to next
        
        # Render sine wave
        self._render_sine_wave()
        
        self.first_render = False
    
    def _render_sine_wave(self):
        """Render the sine wave graph."""
        # Get buffered values
        values = self.sine_graph.buffer.get_display_values()
        
        # Initialize rows with labels
        rows = [label + " " * self.sine_graph.width for label in self.sine_graph.row_labels]
        
        # Plot points with trail effect
        # Only plot if we have actual data in the buffer
        if self.sine_graph.buffer.has_data:
            for i, value in enumerate(values):
                target_row = self.sine_graph._value_to_row(value)
                row_idx = int(round(target_row))
                
                if 0 <= row_idx < self.sine_graph.height:
                    age = len(values) - i - 1
                    if age == 0:
                        char = "●"
                    elif age < 5:
                        char = "•"
                    elif age < 15:
                        char = "·"
                    else:
                        char = "."
                    
                    # Replace character at position
                    pos = len(self.sine_graph.row_labels[0]) + i
                    if pos < len(rows[row_idx]):
                        row_list = list(rows[row_idx])
                        row_list[pos] = char
                        rows[row_idx] = "".join(row_list)
        
        # Add current value indicator
        current_value = self.sine_graph.buffer.get_current_value()
        if current_value is not None:
            current_row = int(round(self.sine_graph._value_to_row(current_value)))
            if 0 <= current_row < self.sine_graph.height:
                rows[current_row] += f" ← Current: {current_value:+.2f}"
        
        # Print all rows
        for row in rows:
            print("\033[2K", end="")  # Clear line
            print(row)


# This module provides terminal graphing functionality as an API
# It should not be executed directly - import and use the classes instead
