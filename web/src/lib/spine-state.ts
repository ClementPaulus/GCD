// Spine state management for five-stop operator loop
export type SpineStage = 'contract' | 'canon' | 'closures' | 'ledger' | 'stance';

export interface SpineState {
  contract?: any;
  canon?: any;
  closures?: any;
  ledger?: any;
  stance?: any;
}
