use anchor_lang::prelude::*;
use anchor_spl::token_interface::{
    self, Mint, Token2022, TokenAccount, Transfer as SplTransfer,
    transfer_checked,
};

declare_id!("BlueWave111111111111111111111111111111111111");

#[program]
pub mod bluewave {
    use super::*;

    /// Transfer BLUEW con 2% de tax a la wallet de marketing
    pub fn transfer_with_tax(
        ctx: Context<TransferWithTax>,
        amount: u64,
        decimals: u8,
    ) -> Result<()> {
        let tax_amount = amount
            .checked_mul(200u64) // 2% = 200 bps
            .unwrap()
            .checked_div(10000u64)
            .unwrap();
        let net_amount = amount.checked_sub(tax_amount).unwrap();

        // Transferir neto al destinatario
        let cpi_program = ctx.accounts.token_program.to_account_info();
        let cpi_accounts = SplTransfer {
            from: ctx.accounts.from.to_account_info(),
            to: ctx.accounts.to.to_account_info(),
            authority: ctx.accounts.authority.to_account_info(),
        };
        let cpi_ctx = CpiContext::new(cpi_program.clone(), cpi_accounts);
        transfer_checked(cpi_ctx, net_amount, decimals)?;

        // Transferir tax a marketing
        let cpi_accounts_tax = SplTransfer {
            from: ctx.accounts.from.to_account_info(),
            to: ctx.accounts.marketing_vault.to_account_info(),
            authority: ctx.accounts.authority.to_account_info(),
        };
        let cpi_ctx_tax = CpiContext::new(cpi_program, cpi_accounts_tax);
        transfer_checked(cpi_ctx_tax, tax_amount, decimals)?;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct TransferWithTax<'info> {
    #[account(mut)]
    pub from: InterfaceAccount<'info, TokenAccount>,

    #[account(mut)]
    pub to: InterfaceAccount<'info, TokenAccount>,

    /// Cuenta de marketing que recibe el 2%
    #[account(mut)]
    pub marketing_vault: InterfaceAccount<'info, TokenAccount>,

    pub authority: Signer<'info>,

    #[account(address = TOKEN_2022_PROGRAM_ID)]
    pub token_program: Interface<'info, Token2022>,

    pub mint: InterfaceAccount<'info, Mint>,
}
