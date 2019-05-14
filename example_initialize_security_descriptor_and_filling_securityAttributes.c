/** Builds security attributes that allows read-only access to everyone
Input parameters: psa: security attributes to build
Output parameters: TRUE | FALSE */ 
BOOL SEC::
    BuildSecurityAttributes( SECURITY_ATTRIBUTES* psa )
{
    DWORD dwAclSize;
    PSID  pSidAnonymous = NULL; // Well-known AnonymousLogin SID
    PSID  pSidOwner = NULL;
    
    if( allocated ) return FALSE;

    SID_IDENTIFIER_AUTHORITY siaAnonymous = SECURITY_NT_AUTHORITY;
    SID_IDENTIFIER_AUTHORITY siaOwner = SECURITY_NT_AUTHORITY;
    
    do
    {
        psd = (PSECURITY_DESCRIPTOR) HeapAlloc( GetProcessHeap(),
                                                HEAP_ZERO_MEMORY,
                                                SECURITY_DESCRIPTOR_MIN_LENGTH);
        if( psd == NULL ) 
        {
            DisplayError( L"HeapAlloc" );
            break;
        }

        if( !InitializeSecurityDescriptor( psd, SECURITY_DESCRIPTOR_REVISION) )
        {
            DisplayError( L"InitializeSecurityDescriptor" );
            break;
        }

        // Build anonymous SID
        AllocateAndInitializeSid( &siaAnonymous, 1, 
                                  SECURITY_ANONYMOUS_LOGON_RID, 
                                  0,0,0,0,0,0,0,
                                  &pSidAnonymous
                                );

        if( !GetUserSid( &pSidOwner ) )
        {
            return FALSE;
        }

        // Compute size of ACL
        dwAclSize = sizeof(ACL) +
                    2 * ( sizeof(ACCESS_ALLOWED_ACE) - sizeof(DWORD) ) +
                    GetLengthSid( pSidAnonymous ) +
                    GetLengthSid( pSidOwner );
      
        pACL = (PACL)HeapAlloc( GetProcessHeap(), HEAP_ZERO_MEMORY, dwAclSize );
        if( pACL == NULL ) 
        {
            DisplayError( L"HeapAlloc" );
            break;
        }
   
        InitializeAcl( pACL, dwAclSize, ACL_REVISION);
   
        
        if( !AddAccessAllowedAce( pACL,
                                  ACL_REVISION,
                                  GENERIC_ALL,
                                  pSidOwner
                                )) 
        {
            DisplayError( L"AddAccessAllowedAce" );
            break;
        }
        
        
        if( !AddAccessAllowedAce( pACL,
                                  ACL_REVISION,
                                  FILE_GENERIC_READ, //GENERIC_READ | GENERIC_WRITE,
                                  pSidAnonymous
                                ) ) 
        {
            DisplayError( L"AddAccessAllowedAce" );
            break;
        }
   
        if( !SetSecurityDescriptorDacl( psd, TRUE, pACL, FALSE) )
        {
            DisplayError( L"SetSecurityDescriptorDacl" );
            break;
        }
      
        psa->nLength = sizeof(SECURITY_ATTRIBUTES);
        psa->bInheritHandle = TRUE;
        psa->lpSecurityDescriptor = psd;

        allocated = TRUE;
    }while(0);

    if( pSidAnonymous )   FreeSid( pSidAnonymous );
    if( pSidOwner )       FreeSid( pSidOwner );
    
    if( !allocated )
    {
        if( psd ) HeapFree( GetProcessHeap(), 0, psd );
        if( pACL ) HeapFree( GetProcessHeap(), 0 , pACL );
    }

    return allocated;
}