import pandas as pd
import json
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, Any
import warnings
warnings.filterwarnings('ignore')

# Visualization setup
plt.style.use('default')
sns.set_palette("husl")

class JSONParsingBenchmark:
    """
    Benchmark class for comparing JSON parsing performance in pandas columns:
    - APPROACH 1: Direct Apply - processes ALL rows including nulls/empty strings
    - APPROACH 2: Masked Apply - uses mask_valid to filter first, then processes only valid rows
    """
    
    def __init__(self, sample_sizes: list = None, fill_rates: list = None):
        self.sample_sizes = sample_sizes or [5000, 25000, 50000, 75000, 100000]
        self.fill_rates = fill_rates or [0.1, 0.3, 0.5, 0.7, 0.9]
        self.results = []
        
    def generate_sample_json(self) -> str:
        """Generate simple JSON with 1-2 fields"""
        json_templates = [
            {"name": f"user_{np.random.randint(1, 1000)}", "age": np.random.randint(18, 80)},
            {"product": f"item_{np.random.randint(1, 500)}", "price": round(np.random.uniform(10, 1000), 2)},
            {"city": f"city_{np.random.randint(1, 100)}"},
            {"status": "active", "count": np.random.randint(1, 100)}
        ]
        return json.dumps(np.random.choice(json_templates))
    
    def create_test_dataframe(self, size: int, fill_rate: float) -> pd.DataFrame:
        """
        Create test DataFrame with given size and fill rate
        Includes realistic empty/invalid cases: None, empty strings, whitespace, invalid JSON
        
        Args:
            size: DataFrame size 
            fill_rate: fraction of rows with valid JSON data (0 to 1)
        """
        json_data = []
        filled_count = int(size * fill_rate)
        empty_count = size - filled_count
        
        # Fill with valid JSON data
        for _ in range(filled_count):
            json_data.append(self.generate_sample_json())
        
        # Fill with various types of empty/invalid data (more realistic)
        empty_types = [
            None,           # Pure None
            '',             # Empty string
            '   ',          # Whitespace only
            '\t\n  ',       # Mixed whitespace
            'null',         # String "null"
            '{}invalid',    # Invalid JSON
            '{broken',      # Malformed JSON
        ]
        
        for _ in range(empty_count):
            # 70% None/empty, 30% invalid JSON strings
            if np.random.random() < 0.7:
                json_data.append(np.random.choice([None, '', '   ', '\t\n  ']))
            else:
                json_data.append(np.random.choice(['null', '{}invalid', '{broken', 'not_json']))
            
        # Shuffle data
        np.random.shuffle(json_data)
        
        return pd.DataFrame({
            'id': range(size),
            'json_column': json_data,
            'other_data': np.random.randn(size)
        })
    
    def parse_json_safe(self, json_str: Optional[str]) -> Optional[Dict[Any, Any]]:
        """Safe JSON parsing with error handling"""
        if json_str is None or pd.isna(json_str):
            return None
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            return None
    
    def approach_1_direct_apply(self, df: pd.DataFrame) -> tuple:
        """
        APPROACH 1: Direct apply to entire series (processes all rows including nulls)
        """
        start_time = time.time()
        result = df['json_column'].apply(self.parse_json_safe)
        end_time = time.time()
        
        return result, end_time - start_time
    
    def approach_2_masked_apply(self, df: pd.DataFrame) -> tuple:
        """
        APPROACH 2: Masked Apply - your approach with proper mask_valid filtering
        Uses comprehensive validation: not null, not empty, not whitespace-only
        """
        start_time = time.time()
        
        # Create comprehensive mask for valid JSON strings (exactly like your example)
        json_series = df['json_column']
        mask_valid = (
            json_series.notna() &                           # Not None/NaN
            (json_series.astype(str).str.strip() != '') &   # Not empty after strip
            (json_series.astype(str).str.strip() != 'nan')  # Not string 'nan'
        )
        
        # Initialize result series with None values
        result = pd.Series(None, index=df.index, dtype='object')
        
        # Early return if no valid data (this is the key optimization!)
        if not mask_valid.any():
            end_time = time.time()
            return result, end_time - start_time
        
        # Extract valid series and apply parsing ONLY to valid entries
        valid_series = json_series[mask_valid]
        parsed_values = valid_series.apply(self.parse_json_safe)
        
        # Assign parsed values back to result
        result.loc[mask_valid] = parsed_values
        
        end_time = time.time()
        return result, end_time - start_time
    
    def run_single_benchmark(self, size: int, fill_rate: float, iterations: int = 3) -> dict:
        """Run benchmark for single parameter combination"""
        print(f"Testing: size={size:,}, fill_rate={fill_rate:.1%}")
        
        times_approach_1 = []
        times_approach_2 = []
        
        for i in range(iterations):
            # Create test data
            df = self.create_test_dataframe(size, fill_rate)
            
            # Approach 1: Direct Apply (processes ALL rows)
            _, time_1 = self.approach_1_direct_apply(df)
            times_approach_1.append(time_1)
            
            # Approach 2: Masked Apply (processes only VALID rows)
            _, time_2 = self.approach_2_masked_apply(df)
            times_approach_2.append(time_2)
        
        avg_time_1 = np.mean(times_approach_1)
        avg_time_2 = np.mean(times_approach_2)
        speedup = avg_time_1 / avg_time_2
        
        return {
            'size': size,
            'fill_rate': fill_rate,
            'direct_apply_time': avg_time_1,
            'masked_apply_time': avg_time_2,
            'direct_apply_std': np.std(times_approach_1),
            'masked_apply_std': np.std(times_approach_2),
            'speedup': speedup,
            'winner': 'Masked Apply' if speedup > 1.0 else 'Direct Apply',
            'time_saved_pct': ((avg_time_1 - avg_time_2) / avg_time_1 * 100) if avg_time_1 > avg_time_2 else 0,
            'mask_benefit': speedup > 1.05  # True if mask provides meaningful benefit (>5%)
        }
    
    def run_full_benchmark(self, iterations: int = 3):
        """Run complete benchmark for all parameter combinations"""
        print("Starting benchmark...")
        
        self.results = []
        
        for size in self.sample_sizes:
            for fill_rate in self.fill_rates:
                result = self.run_single_benchmark(size, fill_rate, iterations)
                self.results.append(result)
        
        self.results_df = pd.DataFrame(self.results)
        print("Benchmark completed!")
        return self.results_df
    
    def print_summary_table(self):
        """Print concise summary table"""
        if not hasattr(self, 'results_df'):
            print("Run benchmark first!")
            return
            
        df = self.results_df
        
        print("\nBENCHMARK RESULTS:")
        print("-" * 80)
        print(f"{'Size':<10} {'Fill%':<8} {'Direct(s)':<12} {'Masked(s)':<12} {'Speedup':<10} {'Winner':<15}")
        print("-" * 80)
        
        for _, row in df.iterrows():
            winner = "Masked" if row['speedup'] > 1.0 else "Direct"
            print(f"{row['size']:<10,} {row['fill_rate']:<8.0%} {row['direct_apply_time']:<12.4f} "
                  f"{row['masked_apply_time']:<12.4f} {row['speedup']:<10.2f} {winner:<15}")
    
    def analyze_results(self):
        """Simple analysis with key findings"""
        if not hasattr(self, 'results_df'):
            print("Run benchmark first!")
            return
            
        df = self.results_df
        self.print_summary_table()
        
        mask_wins = len(df[df['speedup'] > 1.0])
        total_tests = len(df)
        best_speedup = df['speedup'].max()
        best_case = df.loc[df['speedup'].idxmax()]
        
        print(f"\nKEY FINDINGS:")
        print(f"• Masked approach wins: {mask_wins}/{total_tests} tests ({mask_wins/total_tests*100:.1f}%)")
        print(f"• Best speedup: {best_speedup:.2f}x at {best_case['fill_rate']:.0%} fill rate")
        print(f"• Average speedup when masked wins: {df[df['speedup'] > 1.0]['speedup'].mean():.2f}x")
    
    def plot_results(self, figsize: tuple = (12, 5)):
        """Create focused visualization with 2 key charts"""
        if not hasattr(self, 'results_df'):
            print("Run benchmark first!")
            return
            
        df = self.results_df
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle('JSON Parsing: Direct Apply vs Masked Apply Performance', 
                    fontsize=14, fontweight='bold')
        
        # 1. Speedup heatmap
        pivot_speedup = df.pivot(index='fill_rate', columns='size', values='speedup')
        sns.heatmap(pivot_speedup, annot=True, fmt='.2f', cmap='RdYlGn', center=1.0,
                   ax=axes[0], cbar_kws={'label': 'Speedup (Masked/Direct)'})
        axes[0].set_title('Speedup by Fill Rate & Sample Size')
        axes[0].set_xlabel('Sample Size')
        axes[0].set_ylabel('Fill Rate')
        
        # 2. Time savings by fill rate
        savings_stats = df.groupby('fill_rate')['time_saved_pct'].agg(['mean', 'std']).reset_index()
        bars = axes[1].bar(savings_stats['fill_rate'], savings_stats['mean'], 
                          yerr=savings_stats['std'], capsize=5, alpha=0.8)
        
        # Color bars based on savings
        for bar, savings in zip(bars, savings_stats['mean']):
            if savings > 20:
                bar.set_color('darkgreen')
            elif savings > 10:
                bar.set_color('green')
            elif savings > 0:
                bar.set_color('orange')
            else:
                bar.set_color('red')
        
        axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[1].set_xlabel('Fill Rate')
        axes[1].set_ylabel('Average Time Savings (%)')
        axes[1].set_title('Time Savings by Fill Rate')
        axes[1].grid(True, alpha=0.3)
        axes[1].set_xticklabels([f'{int(x*100)}%' for x in savings_stats['fill_rate']])
        
        plt.tight_layout()
        plt.show()
        
        print(f"\nConclusion: Masked approach beneficial in {len(df[df['speedup'] > 1.0])}/{len(df)} tests")
    
    def export_results(self, filename: str = None):
        """Export results to CSV file in results directory"""
        if not hasattr(self, 'results_df'):
            print("Run benchmark first!")
            return
        
        if filename is None:
            import os
            # Create results directory if it doesn't exist
            results_dir = 'results'
            os.makedirs(results_dir, exist_ok=True)
            filename = os.path.join(results_dir, 'json_parsing_benchmark_results.csv')
            
        self.results_df.to_csv(filename, index=False)
        print(f"Results saved to: {filename}")
        return filename

# Demo usage
if __name__ == "__main__":
    print("JSON Parsing Benchmark: Direct Apply vs Masked Apply")
    print("-" * 50)
    
    # Create and run benchmark
    benchmark = JSONParsingBenchmark(
        sample_sizes=[5000, 25000, 50000, 75000, 100000],
        fill_rates=[0.1, 0.3, 0.5, 0.7, 0.9]
    )
    
    results = benchmark.run_full_benchmark(iterations=3)
    benchmark.analyze_results()
    benchmark.plot_results()
    benchmark.export_results()